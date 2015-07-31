from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from datetime import datetime
from .models import Goal, Day
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import streak
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404



def same_date(date1):
    return date1 == datetime.today().date()

def incompleted_goals_with_reminder(user):
    user_goals = user.goal_set.filter(allow_reminders = True)
    return [goal for goal in user_goals if not goal.is_done_today()]

@login_required
def index(request):
    current_user = request.user
    current_goals = Goal.objects.filter(user=current_user)
    all_goals = Goal.objects.all()
    context = {'goals': current_goals, 'all_goals': all_goals}
    return render(request, 'goals/index.html', context)

@login_required
def goal(request, goal_id):
    current_user = request.user
    current_goal = get_object_or_404(Goal, pk=goal_id)
    if current_goal in Goal.objects.filter(user=current_user):
        if request.method=='POST' and not current_goal.is_done_today():
            d = Day(goal=current_goal, date=timezone.now())
            d.save()
        allowed = not current_goal.is_done_today()
        current_user = request.user
        days = current_goal.day_set.all()
        dates = [d.date for d in days]
        lenstreak = streak.cons_dates(dates)
        streakdays = list(current_goal.day_set.all())[-lenstreak:]
        ls = range(lenstreak)
        longest_streak = streak.longest_streak(dates)
        context = {'dates': dates, 'longest_streak':longest_streak, 'streakdays':streakdays, 'days':days, 'current_goal':current_goal, 'lenstreak':lenstreak, 'ls':ls, 'allowed':allowed, 'current_user':current_user}
        return render(request, 'goals/goal.html', context)
    else:
        return HttpResponse('You dont have this goal')

@login_required
def new_goal(request):
    current_user = request.user

    if request.method=='POST':
        new_goal = request.POST['new_goal']
        goal = Goal(user=current_user, name=new_goal, pub_date=timezone.now())
        try:
            goal.save()
            message = 'Nice job!'
        except IntegrityError, e:
            message = e.message
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

@login_required
def about_view(request):
    return render(request, 'goals/about.html')

@login_required
def contact_view(request):
    return render(request, 'goals/contact.html')

@login_required
def update_goal(request, goal_id):
    current_goal = request.user.goal_set.get(id=goal_id)
    current_goal.allow_reminders = 'reminder' in request.POST
    if request.POST['rename'] != '':
        current_goal.name = request.POST['rename']
    current_goal.save()
    return HttpResponseRedirect("/")

@login_required
def mail_view(request):
    users = User.objects.all()
    for user in users:
        goals = incompleted_goals_with_reminder(user)
        if goals and user.email:
            rendered = render_to_string('goals/reminder.html', {'goals': goals})
            msg = EmailMultiAlternatives(
                subject="StreakP reminder",
                body=rendered,
                from_email="streakp@mono.ninja",
                to=[user.email],
            )
            msg.attach_alternative(rendered, "text/html")
            msg.send()
            print 'sending mail to '+ user.email
    return HttpResponse('OK')

