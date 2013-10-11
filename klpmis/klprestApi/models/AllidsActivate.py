from django.core.mail import send_mail
# from klpmis.settings import Boundary, Institution, Programme, Assessment, Question, Student, Staff, StudentGroup
from django.conf import settings
from schools.forms import *
from schools.models import *
from klpmis.settings import *


def hasChildObj(idlists, model_name1):
    modelDict = {
        'boundary': Boundary,
        'institution': Institution,
        'programme': Programme,
        'assessment': Assessment,
        'question': Question,
        'studentgroup': StudentGroup,
        'student': Student,
        'staff': Staff,
        'class': StudentGroup,
        'center': StudentGroup,
    }

        # Checking user Permissions

    haschildlist = []
    for k in idlists:

          # Get Object based on id and model to delete

        obj = modelDict[model_name1.lower()].objects.get(pk=k)
        if model_name1.lower() == 'boundary':
            flag = obj.getChild(obj.boundary_type)
        elif model_name1.lower() in ['class', 'studentgroup']:
            if Student_StudentGroupRelation.objects.filter(
                student_group__id=k, active=2,
                    academic=current_academic()).count():
                flag = True
            else:
                flag = False
        else:
            flag = obj.getChild()

        if flag:
            haschildlist.append(str(k))

    return haschildlist


def SendingMail(idlist, mname, atype):
    inst_liststr = idlist
    sender = settings.REPORTMAIL_SENDER
    receiver = settings.REPORTMAIL_RECEIVER
    if atype == "Deactivated":
        subject = 'Deactivated list'
        fullmsg = 'Following %s Ids are Deactivated  :  \n %s ' % (mname, inst_liststr)
    else:
        subject = 'Activated list'
        fullmsg = 'Following %s Ids are Activated  :  \n %s ' % (mname, inst_liststr)
    send_mail(subject, fullmsg, sender, receiver)
