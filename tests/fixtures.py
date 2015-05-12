# -*- coding: utf-8 -*-
import pytest
from datetime import datetime
from model import EventModel


@pytest.fixture(scope='function')
def events_in_dict():
    return [
        {
            'id': 1,
            'text': 'I just won alottery #update @all',
            'category': '#warn',
            'person': '@all',
            'date': datetime(2015, 1, 16).isoformat()
        },
        {
            'id': 2,
            'text': 'I just won alottery #update @all',
            'category': '#update',
            'person': '@john',
            'date': datetime(2015, 2, 26).isoformat()
        },
        {
            'id': 3,
            'text': 'I just won alottery #update @all',
            'category': '#update',
            'person': '@all',
            'date': datetime(2015, 4, 13).isoformat()
        },
        {
            'id': 4,
            'text': 'I just won alottery #update @all',
            'category': '#update',
            'person': '@john',
            'date': datetime(2015, 4, 1).isoformat()
        }
    ]


@pytest.fixture(scope='function')
def instance_event(events_in_dict):
    event = EventModel(**events_in_dict[0])
    return event.save()


@pytest.fixture(scope='function')
def list_event(events_in_dict):
    response = []
    for event in events_in_dict:
        response.append(EventModel(**event).save())
    return response
