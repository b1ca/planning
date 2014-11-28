# coding=utf-8
from __future__ import unicode_literals


class ChangedTask(object):
    def __init__(self, title, resource, start_date, end_date):
        self.title = title
        self.resource = resource
        self.start_date = start_date
        self.end_date = end_date