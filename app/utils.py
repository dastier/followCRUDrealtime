import json
from datetime import datetime


def generate_op_message(msg):
    payload_dict = json.loads(msg)
    current_time = datetime.now().strftime('%a, %d %b %H:%M:%S')

    if payload_dict['operation'] == 'INSERT':
        verb = 'added'
    elif payload_dict['operation'] == 'UPDATE':
        verb = 'updated'
    else:
        verb = 'removed'

    return "%s:  User \"%s\" with id \"%s\" has been %s" % (
        current_time,
        payload_dict['record']['name'],
        payload_dict['record']['id'],
        verb)
