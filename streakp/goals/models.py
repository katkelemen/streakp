from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from . import streak


class Goal(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    allow_reminders = models.BooleanField(default=False)
    description = models.TextField(null=True)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name

    def is_done_today(self):
        days = self.day_set.all()
        if not days: return False
        else:
            last_entry = days.latest('id').date
            last_entry_date = last_entry.date()
            return last_entry_date == timezone.now().date()

    def lenstreak(self):
        days = self.day_set.all()
        dates = [d.date for d in days]
        return streak.cons_dates(dates)

class Day(models.Model):
    goal = models.ForeignKey(Goal)
    date = models.DateTimeField('date done')

    def __str__(self):
        return str(self.date)
