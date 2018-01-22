import redis
import traceback
import datetime

r = redis.StrictRedis(host='localhost', port=6379, db=5)


def set_step_user(user_id, step):
    r.set(user_id, step)


def get_step_user(user_id):
    try:
        return int(r.get(user_id).decode('utf-8'))
    except KeyError:
        return 0
    except:
        return 0


def set_last_expenses_user(user_id, expenses):
    r.set('id_ex_{}'.format(user_id), expenses)


def get_last_expenses_user(user_id):
    try:
        return int(r.get('id_ex_{}'.format(user_id)).decode('utf-8'))
    except KeyError:
        return 0
    except:
        return 0