from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_reminder_emails()

def incompleted_goals_with_reminder(user):
    user_goals = user.goal_set.filter(allow_reminders = True)
    return [goal for goal in user_goals if not goal.is_done_today()]

def send_reminder_emails():
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
            print user.email
