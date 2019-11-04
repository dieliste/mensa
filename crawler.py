#!/usr/bin/env python3

import os
import re
import requests
import psycopg2

API = 'http://graphite-kom.srv.lrz.de'

# TODO: use homometer model?
def db_update_stats(cursor, stats):
    cursor.executemany(
        '''INSERT INTO homometer_stat (ap, current, timestamp) VALUES (%s,%s,current_timestamp)
                            ON CONFLICT (ap)
                            DO UPDATE SET current = EXCLUDED.current, timestamp = EXCLUDED.timestamp''',
        stats)


def get_stats():
    return requests.get(API + "/render/?from=-1hours&target=ap.ap*-?mg*.ssid.*&format=json").json()


def main():
    conn = psycopg2.connect(host=os.environ['DATABASE_HOST'],
                            dbname=os.environ['DATABASE_NAME'],
                            user=os.environ['DATABASE_USERNAME'],
                            password=os.environ['DATABASE_PASSWORD'])
    cursor = conn.cursor()

    page = get_stats()

    stats = dict()
    aps = list(map(lambda x: (x['target'].split('.')[1], x['datapoints'][-1][0] if x['datapoints'][-1][0] else 0), page))

    for (ap, current) in aps:
        if ap in stats:
            stats[ap] += current
        else:
            stats[ap] = current

    stats = [(k, v) for k, v in stats.items()]

    db_update_stats(cursor, stats)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
