import redis
from .constants import redisHostName, redisPortName, dbName
r = redis.StrictRedis(host=redisHostName, port=redisPortName, db=dbName)


def setex(varname, value, time):
    r.set(varname, value)
    r.expire(varname, time)


def refresh_token(varname):
    r.expire(varname, 900)


def get_token(varname):
    return r.get(varname)


def delete_token(varname):
    return r.delete(varname)


def get_all_fields(field_list_1, field_list_2):
    field_list = list(field_list_1) + list((field_list_2))
    return field_list


def convert_date(date_field, date_format):
    # convert_date will convert the date in given format
    return date_field.strftime(date_format)
