# -*- coding: utf-8 -*-
import argparse
from db import con_params, connect
from model import EventModel
from api import api


def check_con_params():
    if con_params:
        try:
            connect()
        except Exception:
            print('''Error with connection to database. \
                    \nCheck connection parameters in file db.py''')
            return False
        else:
            return True
    else:
        print('Lack of connection parameters in file db.py')
        return False


def server():
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()


parser = argparse.ArgumentParser()
parser.add_argument(
    '--migrate', help='Create table for app', action='store_true')
parser.add_argument('--run', help='Run server', action='store_true')
args = parser.parse_args()
if args.migrate:
    if check_con_params():
        EventModel.create_table()
elif args.run:
    if check_con_params():
        print('Running server on http:\\\\127.0.0.1:8000')
        server()
