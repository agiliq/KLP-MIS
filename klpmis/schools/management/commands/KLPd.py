from django.core.management.base import BaseCommand
from django.db import transaction
from django.core import management

from schools.models import *


class Command(BaseCommand):

    @transaction.autocommit
    def handle(self, *args, **options):
        management.call_command(
            "KLP_callassigncommand",
            assignToUser=[u'71',
                          u'72'],
            userPermission=[u'Acess'],
            permissionType='permissions',
            assessmentId=" ",
            bound_cat="district",
            instName=[],
            boundaryName=[u'9495'],
            assessmentPerm=None)
