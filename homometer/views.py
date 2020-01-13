from django.shortcuts import render
from django.db.models import Sum
from django.views.decorators.clickjacking import xframe_options_exempt
from math import ceil

from .models import Stat


def index(request, minimal=False):
    current = Stat.objects.aggregate(current_sum=Sum('current'))['current_sum']
    current = current if current else 0

    percent = (current / 1500 if current / 1500 < 0.99 else 0.99) * 100 + 1

    colors = ['#2dde57', '#2dde57', '#2dde57', '#f3ad4e', '#f3ad4e', '#f3ad4e', '#f3ad4e', '#ed0009', '#ed0009', '#ed0009']
    color = colors[ceil(percent / 10) - 1]

    context = {
        'current': current,
        'percent': percent,
        'color':   color,
        'minimal': minimal,
    }

    return render(request, 'homometer/index.html', context)


@xframe_options_exempt
def index_minimal(request):
    return index(request, minimal=True)
