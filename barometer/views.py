from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Stat
from math import ceil

def index(request):
    # Unfortunately, Django does not yet allow to filter on window functions :(
    #
    #window = {
    #    'partition_by': [F('ap')],
    #    'order_by': F('timestamp').desc(),
    #}
    #
    #stats = Stat.objects.annotate(
    #    row_number=Window(
    #        expression=RowNumber(), **window,
    #    ),
    #).filter(row_number=1)

    stats = Stat.objects.raw('''WITH latest_stats AS (
            SELECT s.*, ROW_NUMBER() OVER (PARTITION BY ap ORDER BY timestamp DESC) AS rn
            FROM barometer_stat AS s
            )
            SELECT s.id, s.ap, s.max, s.current, s.min, s.avg, s.timestamp FROM latest_stats AS s WHERE rn = 1''')

    current = sum([s.current for s in stats])
    percent = (current / 1500 if current / 1500 < 1 else 1) * 100

    colors = ['#2dde57', '#2dde57', '#2dde57', '#f3ad4e', '#f3ad4e', '#f3ad4e', '#f3ad4e', '#f34e54', '#f34e54', '#f34e54']
    color = colors[ceil(percent / 10) - 1]

    context = {
        'current': current,
        'percent': percent,
        'color': color,
    }

    return render(request, 'barometer/index.html', context)
