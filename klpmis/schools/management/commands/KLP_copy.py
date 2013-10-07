from django.core.management.base import BaseCommand

from schools.models import *


class Command(BaseCommand):

    ''' Command To generate Data Entry Operators History in csv format.'''

    def handle(self, *args, **options):
        questions_list = Question.objects.filter(assessment__id=37)
        asmObj = Assessment.objects.get(id=70)
        for ques in questions_list:
            order = 1
            sMin, sMax, grade = '', '', ''
            if ques.questionType == 1:
                sMin = ques.scoreMin
                sMax = ques.scoreMax
                qObj = Question(
                    assessment=asmObj,
                    name=ques.name,
                    questionType=ques.questionType,
                    scoreMin=sMin,
                    scoreMax=sMax,
                    order=order,
                    active=2)
                qObj.save()
            else:
                grade = ques.grade
                qObj = Question(
                    assessment=asmObj,
                    name=ques.name,
                    questionType=ques.questionType,
                    grade=grade,
                    order=order,
                    active=2)
                qObj.save()
            order = order + 1
