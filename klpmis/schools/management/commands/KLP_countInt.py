import django
import datetime
import os
import csv

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from schools.models import *
from schools.models import *
from klprestApi.TreeMenu import KLP_assignedInstitutions


class Command(BaseCommand):

    ''' Command To map assessments with student group and to assign
    permissions to users automatically. And then it list out
    the user permissions.'''

    def handle(self, *args, **options):
        fileName = 'blore_english_2.csv'
        mapFile = open(fileName, 'r')
        studenGroups = mapFile.read().replace('\n', '')
        mapFile.close()
        sgList = studenGroups.split(',')  # splits student group ids by ,
        s1 = []
        for k in sgList:
            try:
                s1.append(int(k))
            except:
                pass
        v = Institution.objects.filter(studentgroup__id__in=s1).distinct()
        print len(v)
        for instObj in v:
            permInstObj = instObj
            # To generate Institution permission report
            instPermData = []
            boundaryStr = "%s --> %s --> %s" % (
                permInstObj.boundary,
                permInstObj.boundary.parent,
                permInstObj.boundary.parent.parent)
            print boundaryStr
