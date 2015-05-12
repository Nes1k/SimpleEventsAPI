# -*- coding: utf-8 -*-
import falcon
from datetime import datetime
from model import EventModel
from utils import get_event_from_json, dump_attr
api = falcon.API()

PERSON = {'john', 'all', 'all-friends'}
CATEGORY = {'warn', 'update', 'poll'}


class ResourceEvent:

    @dump_attr(id=int)
    def on_get(self, req, resp, id):
        resp.body = EventModel.objects.get_in_json(id=id)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        event_text = get_event_from_json(req.stream.read())
        event_kwargs = EventModel.parse_text(event_text)
        date_time = datetime.now().isoformat()
        EventModel.objects.create(date=date_time, **event_kwargs)
        resp.status = falcon.HTTP_201

    @dump_attr(id=int)
    def on_put(self, req, resp, id):
        event_text = get_event_from_json(req.stream.read())
        event_kwargs = EventModel.parse_text(event_text)
        resp.body = EventModel.objects.update(
            resp_json=True, id=id, **event_kwargs)
        resp.status = falcon.HTTP_200

    @dump_attr(id=int)
    def on_delete(self, req, resp, id):
        EventModel.objects.delete(id=id)
        resp.status = falcon.HTTP_200

api.add_route('/', ResourceEvent())
api.add_route('/{id}/', ResourceEvent())


class ResourceLastEvent:

    @dump_attr(number=int)
    def on_get(self, req, resp, number):
        resp.body = EventModel.objects.all().order_by('date')[number].json()
        resp.status = falcon.HTTP_200

api.add_route('/last/{number}/', ResourceLastEvent())


class ResourceByPerson:

    def on_get(self, req, resp, person):
        if person in PERSON:
            person = '@' + person
            resp.body = EventModel.objects.filter(person=person).json()
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_400

api.add_route('/person/{person}/', ResourceByPerson())


class ResourceByCategory:

    def on_get(self, req, resp, category):
        if category in CATEGORY:
            category = '#' + category
            resp.body = EventModel.objects.filter(category=category).json()
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_400

api.add_route('/category/{category}/', ResourceByCategory())


class ResourceByTime:

    def on_get(self, req, resp, time):
        if len(str(time)) == 6:
            resp.body = EventModel.objects.filter(date=time).json()
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_400

api.add_route('/time/{time}/', ResourceByTime())
