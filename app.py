import falcon
import json

from model import EventModel

api = falcon.API()


class ResourceEvent:

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_201

    def on_put(self, req, resp):
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp):
        resp.status = falcon.HTTP_200

api.add_route('/', ResourceEvent())


class ResourceLastEvent:

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

api.add_route('/last/', ResourceLastEvent())


class ResourceByPerson:

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

api.add_route('/person/', ResourceByPerson())


class ResourceByCategory:

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

api.add_route('/category/', ResourceByCategory())


class ResourceByTime:

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

api.add_route('/time/', ResourceByTime())
