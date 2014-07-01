import string
import time
import django
import datetime
import os
import csv

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):

    @transaction.autocommit
    def handle(self, *args, **options):
        runpath = "python manage.py"
        exefile = ""
        try:
            # Reads the arguments from command line.
            prgram = programme = options["scriptname"]
        except:
            program = programme = "KLP_permission.py"
        try:
            ss = os.spawnlp(os.P_WAIT, 'python', 'python', 'timesleep.py')
        except AttributeError:
            print "EROOR"
        try:
            spawnv = os.spawnv
        except AttributeError:
            # assume it's unix
            pid = os.fork()
            if not pid:
                os.execvp(program, (program,) + args)
                return os.wait()[0]
        else:
                # got spawnv but no spawnp: go look for an executable
            for path in string.split(os.environ["PATH"], os.pathsep):
                file = os.path.join(path, program) + exefile
                try:
                    return spawnv(os.P_WAIT, file, (file,) + args)
                except os.error:
                    pass
            raise IOError("cannot find executable")
