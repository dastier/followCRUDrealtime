import os
import multiprocessing
import select

import psycopg2
import psycopg2.extensions

# hostname = 'localhost'
# username = 'postgres'
# password = 'mysecretpassword'
# database = 'postgres'

DATABASE_URI = os.environ['DATABASE_URL']

class MyFancyClass(object):

    def __init__(self, name):
        self.name = name

    def do_something(self):
        proc_name = multiprocessing.current_process().name
        # conn = psycopg2.connect(host=hostname, user=username,
        #                         password=password, database=database)
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
                    print ('Doing something with websockets here! in %s for %s!' % (proc_name, self.name))


def worker(q):
    obj = q.get()
    obj.do_something()


if __name__ == '__main__':
    queue = multiprocessing.Queue()

    p = multiprocessing.Process(target=worker, args=(queue,))
    p.start()

    queue.put(MyFancyClass('Fancy Dan'))

    # Wait for the worker to finish
    queue.close()
    queue.join_thread()
    p.join()
