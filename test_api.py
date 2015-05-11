import pytest
import multiprocessing
import requests
import random

from app import api


def server_config(port):

    def server():
        from wsgiref import simple_server
        httpd = simple_server.make_server('127.0.0.1', port, api)
        httpd.serve_forever()

    return server


@pytest.yield_fixture(scope='function')
def server():
    '''
    This yield fixture allows run many tests from test_appi
    simultaneously with xdist plugin for py.test

    To send tests to multiple CPUs, type:
    py.test test_api.py -n NUM
    '''
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

    def test_get(self, server):
        r = requests.get(server)
        assert r.status_code == 200

    def test_post(self, server):
        r = requests.post(server)
        assert r.status_code == 201

    def test_put(self, server):
        r = requests.put(server)
        assert r.status_code == 200

    def test_delete(self, server):
        r = requests.delete(server)
        assert r.status_code == 200

    def test_last_get(self, server):
        r = requests.get(server + '/last/')
        assert r.status_code == 200

    def test_by_person_get(self, server):
        r = requests.get(server + '/person/')
        assert r.status_code == 200

    def test_by_category_get(self, server):
        r = requests.get(server + '/category/')
        assert r.status_code == 200

    def test_by_time_get(self, server):
        r = requests.get(server + '/time/')
        assert r.status_code == 200
