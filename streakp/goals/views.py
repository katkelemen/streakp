from django.shortcuts import render

from .models import Goal


def index(request):

    v1 = Goal.objects.all()

    context = {'goals': v1}
    return render(request, 'goals/index.html', context)
