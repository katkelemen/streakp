from django.contrib import admin
from models import Day, Achievement
from models import Goal
from models import Credit

class DayInline(admin.TabularInline):
    model = Day
    extra = 3

class GoalAdmin(admin.ModelAdmin):
    inlines = [DayInline]
    list_filter = ['pub_date']
    list_display = ('name', 'pub_date', 'user')

admin.site.register(Goal, GoalAdmin)
admin.site.register(Credit)
admin.site.register(Achievement)

