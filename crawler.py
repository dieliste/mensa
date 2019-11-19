#!/usr/bin/env python3

import os
import django
import re
import requests
import psycopg2

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mensa.settings")
django.setup()

from homometer.models import Stat


API = 'http://graphite-kom.srv.lrz.de'


def db_update_stats(stats):
    for k, v in stats:
        Stat.objects.update_or_create(
            ap=k,
            defaults={'current': v},
        )


def get_stats():
    return requests.get(API + "/render/?from=-1hours&target=ap.ap*-?mg*.ssid.*&format=json").json()


def main():
    page = get_stats()

    stats = dict()
    aps = list(map(lambda x: (x['target'].split('.')[1], x['datapoints'][-1][0] if x['datapoints'][-1][0] else x['datapoints'][-2][0] if x['datapoints'][-2][0] else 0), page))

    for (ap, current) in aps:
        if ap in stats:
            stats[ap] += current
        else:
            stats[ap] = current

    stats = [(k, v) for k, v in stats.items()]

    db_update_stats(stats)


if __name__ == "__main__":
    main()
