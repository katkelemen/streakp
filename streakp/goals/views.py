from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from datetime import datetime
from .models import Goal, Day
from django.contrib.auth import authenticate, login


def same_date(date1):
    return date1 == datetime.today().date()


def allow_create(goal):
    days = goal.day_set.all()
    if not days: return True
    else:
        last_entry = days.latest('id').date
        last_entry_date = last_entry.date()
        return last_entry_date != timezone.now().date()


def index(request):
    current_user = request.user
    current_goals = Goal.objects.filter(user=current_user)

    context = {'goals': current_goals}
    return render(request, 'goals/index.html', context)


def goal(request, goal_id):
    current_goal = Goal.objects.get(id=goal_id)
    days = current_goal.day_set.all()
    context = {'days': days, 'current_goal':current_goal}
    if request.method=='POST' and allow_create(current_goal):
        d = Day(goal=current_goal, date=timezone.now())
        d.save()
        return render(request, 'goals/goal.html', context)
    else:
        return render(request, 'goals/goal.html', context)

def new_goal(request):
    current_user = request.user

    if request.method=='POST':
        new_goal = request.POST['new_goal']
        goal = Goal(user=current_user, name=new_goal, pub_date=timezone.now())
        try:
            goal.save()
            message = 'Nice job!'
        except IntegrityError:
            message = 'You already created this goal'
        current_goals = Goal.objects.filter(user=current_user)
        context = {'goals': current_goals, 'message': message}
        return render(request, 'goals/index.html', context)


def loginview(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                # Return a 'disabled account' error message
                HttpResponse('Disabled account')
        else:
            # Return an 'invalid login' error message.
            HttpResponse('invalid login')
    else:
        return render(request, 'goals/login.html')