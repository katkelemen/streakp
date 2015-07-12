from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from datetime import datetime
from .models import Goal, Day
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import streak


def same_date(date1):
    return date1 == datetime.today().date()


def allow_create(goal):
    days = goal.day_set.all()
    if not days: return True
    else:
        last_entry = days.latest('id').date
        last_entry_date = last_entry.date()
        return last_entry_date != timezone.now().date()


@login_required
def index(request):
    current_user = request.user
    current_goals = Goal.objects.filter(user=current_user)

    context = {'goals': current_goals}
    return render(request, 'goals/index.html', context)

@login_required
def goal(request, goal_id):
    current_goal = Goal.objects.get(id=goal_id)
    days = current_goal.day_set.all()
    dates = [d.date for d in days]
    lenstreak = streak.cons_dates(dates)
    ls = range(lenstreak)
    context = {'days': days, 'current_goal':current_goal, 'lenstreak':lenstreak, 'ls':ls}
    if request.method=='POST' and allow_create(current_goal):
        d = Day(goal=current_goal, date=timezone.now())
        d.save()
        return render(request, 'goals/goal.html', context)
    else:
        return render(request, 'goals/goal.html', context)

@login_required
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


def login_view(request):
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
                return HttpResponse('Disabled account')
        else:
            # Return an 'invalid login' error message.
            return HttpResponse('invalid login')
    else:
        return render(request, 'goals/login.html')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login/")
    # Redirect to a success page.


@login_required
def delete_goal(request, goal_id):
    current_goal = request.user.goal_set.get(id=goal_id)
    current_goal.delete()
    return HttpResponseRedirect("/")

def probe_view(request):
    return render(request, 'goals/probe.html')

def about_view(request):
    return render(request, 'goals/about.html')

def contact_view(request):
    return render(request, 'goals/contact.html')
