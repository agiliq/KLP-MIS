#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core import serializers


def get_all_data(entry):
    serial = serializers.serialize('python', [entry])[0]
    serial['fields'][entry._meta.pk.name] = serial['pk']
    return serial['fields']

