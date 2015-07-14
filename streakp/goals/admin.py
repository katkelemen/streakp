from django.contrib import admin
from models import Day
from models import Goal

class DayInline(admin.TabularInline):
    model = Day
    extra = 3


class GoalAdmin(admin.ModelAdmin):
    inlines = [DayInline]
    list_filter = ['pub_date']
    list_display = ('name', 'pub_date', 'user')

admin.site.register(Goal, GoalAdmin)

