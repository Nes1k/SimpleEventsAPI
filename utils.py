# -*- coding: utf-8 -*-
from functools import wraps, partial
import json
import falcon


def get_result_json(raw_json):
    try:
        result_json = json.loads(raw_json.decode('utf-8'))
    except ValueError:
        raise falcon.HTTPBadRequest('Bad json format')
    return result_json


def get_event_from_json(raw_json):
    result_json = get_result_json(raw_json)
    try:
        event = result_json['event']
    except KeyError:
        raise falcon.HTTPBadRequest('Bad request, missing event param.')
    return event


def dump_attr(func=None, **params):
    if func is None:
        return partial(dump_attr, **params)

    @wraps(func)
    def wrapper(*args, **kwargs):
        for key, value in params.items():
            try:
                kwargs[key] = value(kwargs[key])
            except (ValueError, KeyError):
                raise falcon.HTTPBadRequest(
                    'Bad request', 'Bad parametrs %s' % key)
        return func(*args, **kwargs)

    return wrapper
