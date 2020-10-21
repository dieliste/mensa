from django.shortcuts import render
from django.db.models import Sum
from django.views.decorators.clickjacking import xframe_options_exempt
from math import floor

from .models import Stat


def index(request, minimal=False):
    # It would be nice if the aggregate function could return a default value when
    # there are no rows: https://code.djangoproject.com/ticket/10929
    current = Stat.objects.aggregate(current_sum=Sum('current'))['current_sum']
    current = current if current else 0

    # clip current to range [0, 1500] and convert to percent
    percent = (sorted([0, current, 1500])[1] / 1500) * 100

    colors = ['#2dde57', '#2dde57', '#2dde57', '#f3ad4e', '#f3ad4e', '#f3ad4e', '#f3ad4e', '#ed0009', '#ed0009', '#ed0009', '#ed0009']
    color = colors[floor(percent / 10)]

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
