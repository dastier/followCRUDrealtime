#!/usr/bin/python3
import select

import psycopg2
import psycopg2.extensions

hostname = 'localhost'
username = 'postgres'
password = 'mysecretpassword'
database = 'postgres'

conn = psycopg2.connect(host=hostname, user=username,
                        password=password, database=database )
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

curs = conn.cursor()
curs.execute("LISTEN events;")

print ("Waiting for notifications on channel 'events'")
while True:
    if select.select([conn],[],[],5) == ([],[],[]):
        print ("Timeout")
    else:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            print ("Got NOTIFY:", notify.payload)
