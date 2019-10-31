#!/usr/bin/env python3

import os
import psycopg2


def db_setup(cursor):
    cursor.execute('CREATE TABLE IF NOT EXISTS barometer_stat_permanent ( like barometer_stat including all)')


def backup_data(cursor):
    cursor.execute('''WITH latest_stats AS (
        SELECT s.*, ROW_NUMBER() OVER (PARTITION BY ap ORDER BY timestamp DESC) AS rn
        FROM barometer_stat AS s
        )
        INSERT INTO barometer_stat_permanent
        SELECT s.id, s.ap, s.max, s.current, s.min, s.avg, s.timestamp
        FROM latest_stats AS s
        WHERE rn = 1''')


def clean_db(cursor):
    cursor.execute('DELETE FROM barometer_stat WHERE timestamp < NOW() - INTERVAL \'1 day\'')


def main():
    conn = psycopg2.connect(host=os.environ['DATABASE_HOST'],
                            dbname=os.environ['DATABASE_NAME'],
                            user=os.environ['DATABASE_USERNAME'],
                            password=os.environ['DATABASE_PASSWORD'])
    cursor = conn.cursor()

    db_setup(cursor)
    backup_data(cursor)
    clean_db(cursor)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
