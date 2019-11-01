from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum

from .models import Stat
from math import ceil

def index(request):
    current = Stat.objects.aggregate(current_sum=Sum('current'))['current_sum']
    current = current if current else 0

    percent = (current / 1500 if current / 1500 < 1 else 1) * 100

    colors = ['#2dde57', '#2dde57', '#2dde57', '#f3ad4e', '#f3ad4e', '#f3ad4e', '#f3ad4e', '#ed0009', '#ed0009', '#ed0009']
    color = colors[ceil(percent / 10) - 1]

    context = {
        'current': current,
        'percent': percent,
        'color': color,
    }

    return render(request, 'homometer/index.html', context)
