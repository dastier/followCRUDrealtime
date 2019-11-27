import json


def generate_user_message(msg):
        payload_dict = json.loads(msg)

        if payload_dict['operation'] == 'INSERT':
            verb = 'added'
        elif payload_dict['operation'] == 'UPDATE':
            verb = 'updated'
        else:
            verb = 'removed'

        return "User %s with id %s has been %s" % (payload_dict['record']['name'],
                                                   payload_dict['record']['id'],
                                                   verb)
