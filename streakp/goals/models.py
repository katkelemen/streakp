from django.db import models

class Goal(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.name

class Day(models.Model):
    goal = models.ForeignKey(Goal)
    date = models.DateTimeField('date done')

    def __str__(self):
        return str(self.date)