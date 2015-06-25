from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import Goal, Day


def index(request):

    v1 = Goal.objects.all()

    context = {'goals': v1}
    return render(request, 'goals/index.html', context)

def goal(request, goal_id):
    current_goal = Goal.objects.get(id=goal_id)
    days = current_goal.day_set.all()
    context = {'days': days, 'current_goal':current_goal}

    if request.method=='POST':
        d = Day(goal=current_goal, date=timezone.now())
        d.save()
        return HttpResponse("OK, created!")
    else:
        return render(request, 'goals/goal.html', context)
