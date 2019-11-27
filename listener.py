import os
import select
import threading
import json

import psycopg2
import psycopg2.extensions

DATABASE_URI = os.environ['DATABASE_URL']


class myThread (threading.Thread):
    def __init__(self, name, counter):
        threading.Thread.__init__(self)
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting %s" % self.name)
        MyFancyClass.do_something(self)
        print("Exiting %s" % self.name)


class MyFancyClass(object):

    def __init__(self, name):
        self.name = name

    def do_something(self):
        from app import send_mymsg
        conn = psycopg2.connect(DATABASE_URI)
        conn.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        curs = conn.cursor()
        curs.execute("LISTEN events;")

        print("Waiting for notifications on channel 'events'")
        while True:
            if select.select([conn], [], [], 5) == ([], [], []):
                print("Timeout")
            else:
                conn.poll()
                while conn.notifies:
                    notify = conn.notifies.pop(0)
                    msg = self.generate_user_message(notify)
                    send_mymsg(msg)
                    
                    print("Got NOTIFY:", notify.payload)
                    f = open("/tmp/NOTIFY", "w+")
                    f.write(("notified! got: %s" % notify.payload))
                    f.close()
    
    def generate_user_message(self, msg):
        # payload = '{"operation" : "INSERT", "record" : {"id":13,"name":"hello"}}'
        payload_dict = json.loads(msg)
        db_operation = payload_dict['operation']
        user_id = payload_dict['record']['id']
        user_name = payload_dict['record']['name']

        if db_operation == 'INSERT':
            verb = 'added'
        elif db_operation == 'UPDATE':
            verb = 'updated'
        else:
            verb = 'removed'


        return "User %s with id %s was %s" % (user_name, user_id, verb)