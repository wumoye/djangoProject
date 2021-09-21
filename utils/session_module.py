import json

from django_redis import get_redis_connection


def set_session(key, val):
    con = get_redis_connection('session')
    res = con.set(f"user:{key}", json.dumps(val), 60 * 60 * 24)

    return res


def get_session(key):
    con = get_redis_connection('session')
    val = eval(con.get(f"user:{key}").decode("utf-8"))

    return val
