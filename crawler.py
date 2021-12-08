#!/usr/bin/env python3

import os
import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mensa.settings")
django.setup()

from homometer.models import Stat


def get_stats():
    return requests.get("http://graphite-kom.srv.lrz.de/render/?from=-1hours&target=ap.ap*-?mg*.ssid.*&format=json").json()


def update_stats(stats):
    for k, v in stats.items():
        Stat.objects.update_or_create(
            ap=k,
            defaults={'current': v},
        )


def main():
    page = get_stats()

    aps = list(map(lambda x: (x['target'].split('.')[1], x['datapoints'][-1][0]
                                or x['datapoints'][-2][0] or 0), page))

    stats = dict()
    for ap, current in aps:
        if ap in stats:
            stats[ap] += current
        else:
            stats[ap] = current

    update_stats(stats)


if __name__ == "__main__":
    main()
