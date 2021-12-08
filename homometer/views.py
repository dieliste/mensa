from math import floor

from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from .models import Stat


def get_current_and_percent():
    # It would be nice if the aggregate function could return a default value when
    # there are no rows: https://code.djangoproject.com/ticket/10929
    current = Stat.objects.aggregate(Sum('current'))['current__sum'] or 0

    # clip current to range [0, 1500] and convert to percent
    percent = sorted([0, current, 1500])[1] / 1500 * 100

    return current, percent


def api(request):
    current, percent = get_current_and_percent()
    return JsonResponse({"current": current, "percent": percent})


def index(request, minimal=False):
    current, percent = get_current_and_percent()

    # determine homometer color
    colors = ['#2dde57', '#f3ad4e', '#ed0009', '#ed0009']
    color = colors[floor(percent / 100 * (len(colors) - 1))]

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
