#!/usr/bin/env python

import calendar
import datetime
import os
import sys
import json

import psycopg2

REQ_ENV_VARS = ['BDM_PG_HOST',
                'BDM_PG_USER',
                'BDM_PG_PASSWORD',
                'BDM_PG_MGMT_DBNAME',
                ]

# each optional item consists of a tuple (var_name, default_value)
OPT_ENV_VARS = [('BDM_PG_PORT', 5432),
                ('BDMD_DEBUG', 0),
                ]

if __name__ == '__main__':
    if not (2 <= len(sys.argv) <= 3):
        print("USAGE %s output_filename.json [DOWNTIME_THRESHOLD=180]"
              % sys.argv[0])
        sys.exit(2)
    f = open(sys.argv[1], 'w')
    if len(sys.argv) == 3:
        DOWNTIME_THRESHOLD = datetime.timedelta(seconds=int(sys.argv[2]))
    else:
        DOWNTIME_THRESHOLD = datetime.timedelta(seconds=180)

    config = {}
    for evname in REQ_ENV_VARS:
        try:
            config[evname] = os.environ[evname]
        except KeyError:
            print(("Environment variable '%s' required and not defined. "
                    "Terminating.") % evname)
            sys.exit(1)
    for (evname, default_val) in OPT_ENV_VARS:
        config[evname] = os.environ.get(evname) or default_val

    mconn = psycopg2.connect(
            host=config['BDM_PG_HOST'],
            port=int(config['BDM_PG_PORT']),
            database=config['BDM_PG_MGMT_DBNAME'],
            user=config['BDM_PG_USER'],
            password=config['BDM_PG_PASSWORD'],
            )

    mcur = mconn.cursor()
    mcur.execute(
            "SELECT id, date_seen "
            "FROM devices_log "
            "ORDER BY id, date_seen;")
    data = mcur.fetchall()
    intervals_by_id = {}
    current_id = None
    current_intervals = []
    interval_start = None
    interval_end = None
    for row in data:
        if row[0] != current_id:
            if current_id is not None:
                current_intervals.append(
                        (calendar.timegm(interval_start.timetuple())*1000,
                        calendar.timegm(interval_end.timetuple())*1000))
                intervals_by_id[current_id] = (zip(*current_intervals))
                current_intervals = []
            current_id = row[0]
            interval_start = row[1]
            interval_end = row[1]
        else:
            if (row[1] - interval_end) > DOWNTIME_THRESHOLD:
                current_intervals.append(
                        (calendar.timegm(interval_start.timetuple())*1000,
                        calendar.timegm(interval_end.timetuple())*1000))
                interval_start = row[1]
            interval_end = row[1]
    current_intervals.append(
            (calendar.timegm(interval_start.timetuple())*1000,
            calendar.timegm(interval_end.timetuple())*1000))
    intervals_by_id[current_id] = (zip(*current_intervals))

    json.dump(
            (intervals_by_id,
            calendar.timegm(datetime.datetime.utcnow().timetuple())*1000),
            f)
    f.close()
