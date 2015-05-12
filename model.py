# -*- coding: utf-8 -*-
from db import Model, Field, execute_sql


class EventModel(Model):
    text = Field(blank=False)
    category = Field(blank=False)
    person = Field(blank=False)
    date = Field(blank=False)

    @staticmethod
    def parse_text(text):
        response = {'text': text, 'category': '#update', 'person': '@all'}
        words = text.split(' ')
        for word in words:
            if word.startswith('#'):
                response['category'] = word
            elif word.startswith('@'):
                response['person'] = word
        return response

    @staticmethod
    def create_table():
        execute_sql('''CREATE TABLE eventmodel (
                        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                        text TEXT,
                        category CHAR(7),
                        person char(12),
                        date DATETIME
        )''')
