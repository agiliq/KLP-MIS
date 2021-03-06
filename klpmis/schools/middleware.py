#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Print the query log to standard out.

Useful for optimizing database calls.

Insipired by the method at: <http://www.djangosnippets.org/snippets/344/>
"""

from django.conf import settings
from django.db import connection


class QueryLogMiddleware:

    def process_response(self, request, response):
        if settings.DEBUG:
            queries = {}
            for query in connection.queries:
                sql = query['sql']
                queries.setdefault(sql, 0)
                queries[sql] += 1
        return response


