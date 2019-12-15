import os
import select
import threading

import psycopg2
import psycopg2.extensions

from utils import generate_op_message

DATABASE_URI = os.environ['DATABASE_URL']


class myThread (threading.Thread):
    def __init__(self, name, counter):
        threading.Thread.__init__(self)
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting %s" % self.name)
        Listener.listen(self)
        print("Exiting %s" % self.name)


class Listener(object):
    def __init__(self, name):
        self.name = name

    def listen(self):
        from app import send_op_msg
        conn = psycopg2.connect(DATABASE_URI)
        conn.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        curs = conn.cursor()
        curs.execute("LISTEN events;")

        print("Waiting for notifications on channel 'events'")
        while True:
            if select.select([conn], [], [], 5) == ([], [], []):
                pass
            else:
                conn.poll()
                while conn.notifies:
                    notify = (conn.notifies.pop(0))
                    send_op_msg(generate_op_message(notify.payload))
