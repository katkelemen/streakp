from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta
from . import streak


class Goal(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    allow_reminders = models.BooleanField(default=False)
    description = models.TextField(null=True)
    notes = models.TextField(null=True)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name

    def is_done_today(self):
        days = self.day_set.all()
        if not days:
            return False
        else:
            today = timezone.now().date()
            filtered_days = self.day_set.filter(date__year=today.year, date__month=today.month, date__day=today.day)
            return filtered_days.count() > 0

    def is_done_yesterday(self):
        days = self.day_set.all()
        if not days:
            return False
        else:
            yesterday = timezone.now().date() - timedelta(days=1)
            filtered_days = self.day_set.filter(
                date__year=yesterday.year,
                date__month=yesterday.month,
                date__day=yesterday.day
            )
            return filtered_days.count() > 0

    def lenstreak(self):
        days = self.day_set.all()
        dates = [d.date for d in days]
        return streak.cons_dates(dates)

    def user_has_credit(self):
        credit = Credit.objects.get(user=self.user).credit
        return credit > 0


class Day(models.Model):
    goal = models.ForeignKey(Goal)
    date = models.DateTimeField('date done')

    def __str__(self):
        return str(self.date)

    class Meta:
        ordering = ['date']


class Credit(models.Model):
    user = models.ForeignKey(User)
    credit = models.IntegerField(default=1)

    def __unicode__(self):
        return '%d' % (self.credit)

class Achievement(models.Model):
    user = models.ForeignKey(User)
    reason = models.TextField()

    def __unicode__(self):
        return '%s' % (self.reason)
