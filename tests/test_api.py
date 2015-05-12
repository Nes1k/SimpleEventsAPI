# -*- coding: utf-8 -*-r
import pytest
import multiprocessing
import requests
import random
import json

from .fixtures import *
from model import EventModel
import db
from app import api


def server_config(port):

    def server():
        from wsgiref import simple_server
        httpd = simple_server.make_server('127.0.0.1', port, api)
        httpd.serve_forever()

    return server


@pytest.yield_fixture(scope='function')
def server():
    port = random.randint(4000, 9000)
    while True:
        try:
            requests.get('http://127.0.0.1:' + str(port))
        except requests.exceptions.ConnectionError:
            break
        else:
            port = random.randint(4000, 9000)
    process = multiprocessing.Process(target=server_config(port))
    process.deamon = True
    process.start()
    process.join(1)
    url = 'http://127.0.0.1:' + str(port)
    yield url
    process.terminate()


class TestResource:

    @classmethod
    def setup_class(cls):
        EventModel.create_table()

    @classmethod
    def teardown_class(cls):
        db.execute_sql('DROP TABLE eventmodel')

    def teardown(self):
        db.execute_sql('TRUNCATE eventmodel')

    def test_get(self, server, list_event, events_in_dict):
        r = requests.get(server + '/2/')
        assert r.json() == events_in_dict[1]
        assert r.status_code == 200

    def test_post(self, server):
        event = {'event': 'I just won alottery #update @all'}
        r = requests.post(server, data=json.dumps(event))
        assert r.status_code == 201
        assert EventModel.objects.count() == 1

    def test_put(self, server, list_event):
        event = {'event': 'I just won alottery #warn @john'}
        r = requests.put(server + '/2/', data=json.dumps(event))
        assert r.status_code == 200
        assert r.json() == {
            'id': 2,
            'text': 'I just won alottery #warn @john',
            'category': '#warn',
            'person': '@john',
            'date': datetime(2015, 2, 26).isoformat()
        }

    def test_delete(self, server, list_event):
        r = requests.delete(server + '/3/')
        assert r.status_code == 200
        assert EventModel.objects.count() == 3

    def test_last_get(self, server, list_event):
        r = requests.get(server + '/last/2/')
        assert r.status_code == 200
        assert len(r.json()) == 2

    def test_by_person_get(self, server, list_event):
        r = requests.get(server + '/person/all/')
        assert r.status_code == 200
        assert len(r.json()) == 2

    def test_by_category_get(self, server, list_event):
        r = requests.get(server + '/category/warn/')
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_by_time_get(self, server, list_event):
        r = requests.get(server + '/time/150226/')
        assert r.status_code == 200
        assert len(r.json()) == 1
