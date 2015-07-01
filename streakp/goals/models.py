from django.contrib.auth.models import User
from django.db import models


class Goal(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name

class Day(models.Model):
    goal = models.ForeignKey(Goal)
    date = models.DateTimeField('date done')

    def __str__(self):
        return str(self.date)