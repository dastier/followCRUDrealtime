import os
import select
import threading

import psycopg2
import psycopg2.extensions

# hostname = 'localhost'
# username = 'postgres'
# password = 'mysecretpassword'
# database = 'postgres'

DATABASE_URI = os.environ['DATABASE_URL']

class myThread (threading.Thread):
   def __init__(self, name, counter):
      threading.Thread.__init__(self)
      self.name = name
      self.counter = counter
   def run(self):
      print ("Starting %s" % self.name)
      MyFancyClass.do_something(self)
      print ("Exiting %s" % self.name)

class MyFancyClass(object):

    def __init__(self, name):
        self.name = name

    def do_something(self):
        conn = psycopg2.connect(DATABASE_URI)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        curs = conn.cursor()
        curs.execute("LISTEN events;")

        print ("Waiting for notifications on channel 'events'")
        while True:
            if select.select([conn], [], [], 5) == ([], [], []):
                print ("Timeout")
            else:
                conn.poll()
                while conn.notifies:
                    notify = conn.notifies.pop(0)
                    print ("Got NOTIFY:", notify.payload)
                    print ('Doing something with websockets here! for %s!' % (self.name))
                    f=open("/tmp/NOTIFY","w+")
                    f.write(("notified! got: %s" % notify.payload))
                    f.close()
