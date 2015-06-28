from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime
from .models import Goal, Day

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
    v1 = Goal.objects.filter(user=current_user)

    context = {'goals': v1}
    return render(request, 'goals/index.html', context)


def goal(request, goal_id):
    current_goal = Goal.objects.get(id=goal_id)
    days = current_goal.day_set.all()
    context = {'days': days, 'current_goal':current_goal}
    if request.method=='POST' and allow_create(current_goal):
        d = Day(goal=current_goal, date=timezone.now())
        d.save()
        return render(request, 'goals/goal.html', context)
            #HttpResponse("OK, created!")
    else:
        return render(request, 'goals/goal.html', context)