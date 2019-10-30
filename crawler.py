#!/usr/bin/env python3

import os
import re
import requests
import psycopg2

API = 'http://wlan.lrz.de'


def db_update_stats(cursor, stats):
    cursor.executemany('INSERT INTO barometer_stat (ap, max, current, min, avg, timestamp) VALUES (%s,%s,%s,%s,%s,current_timestamp)', stats)


def get_stats():
    return requests.get(API + "/apstat/").text


def main():
    conn = psycopg2.connect(host=os.environ['DATABASE_HOST'],
                            dbname=os.environ['DATABASE_NAME'],
                            user=os.environ['DATABASE_USERNAME'],
                            password=os.environ['DATABASE_PASSWORD'])
    cursor = conn.cursor()

    page = get_stats()

    # creepy regex, do not touch unless you know what you do
    p = re.compile('Neubau Mensa Garching.+?/apstat/(.+?(?=/")).+?\(([\d\.]+) - ([\d\.]+) - ([\d\.]+) - ([\d\.]+)(?=\))', re.S)
    stats = p.findall(page)

    db_update_stats(cursor, stats)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
