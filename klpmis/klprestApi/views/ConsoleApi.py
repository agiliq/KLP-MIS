#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
ConsoleApi is used to run raw sql queries from frontend.
"""
import psycopg2
from django.http import HttpResponse
import simplejson

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType

from fullhistory.models import Request, FullHistory
from django.conf import settings


def KLP_Admin_Console(request):
    ''' To show the admin Console to run SQl Queries '''

    user = request.user
    context = {'title': 'Karnataka Learning Partnership ',
               'user': user}

    return render(request,
                  'viewtemplates/admin_console.html',
                  context)


@csrf_exempt
def KLP_Run_Query(request):
    ''' To run SQl Queries Entered by admin'''

    DATABASES = settings.DATABASES
    # get query to perform
    adminQuery = request.POST.get('form-staging-query')

    # connection = sqlite.connect('/home/klp/klp/klp.db')
    # Establish connection with postgresql by passing dbname,
            # user name and password.

    d = DATABASES['default']
    datebase = d['NAME']
    user = d['USER']
    password = d['PASSWORD']
    connection = psycopg2.connect(database=datebase, user=user,
                                  password=password)
    cursor = connection.cursor()
    isExecute = False
    if adminQuery:
        try:

            # execute query

            cursor.execute(adminQuery)

            # transaction.commit_unless_managed()
            # If query executes fine return response as
                # "Query Executed Sucessfully"

            connection.commit()
            storeFullhistory(request)
            respStr = 'Query Executed Sucessfully .'
            isExecute = True
        except:

            # else return response as "Query You Written
            # May Incorrect, Please Check It"

            respStr = \
                'Query You Written May Incorrect, Please Check It.'
    else:

        # If query is empty return response as "Query You Send Is Empty"

        respStr = 'Query You Send Is Empty'

    # close connection

    cursor.close()
    respDict = {'respStr': respStr, 'isExecute': isExecute}
    return HttpResponse(simplejson.dumps(respDict),
                        content_type='application/json; charset=utf-8')


def storeFullhistory(requestparam):
    username = requestparam.user
    userid = requestparam.user.id
    adminQuery = requestparam.POST.get('form-staging-query')
    action = adminQuery[0].upper()
    fullrequest = Request(user_name=username, user_pk=userid,
                          request_path='/console/')
    fullrequest.save()

    objid = 0
    data = adminQuery

    if 1:
        if action == 'I':
            objname = adminQuery.split('schools_')[1].split('(')[0].strip()
        else:
            objname = adminQuery.split('schools_')[1].split(' ')[0]

        try:
            obj = ContentType.objects.filter(model=objname)[0]

            content_type_id = obj.id
        except:
            content_type_id = 4
        if 1:
            if action == 'I':
                objid = 0
            # objdic[objname].objects.all().aggregate(Max('id'))['id__max']
            elif action in ['U', 'D']:
                objid = adminQuery.split('where')[1].split('id=')
                if objid:
                    objid = (objid[1])[:-1]
        else:
            objid = 0
    else:

        obj = ''
    try:
        create_info = create_infos(requestparam, action)
    except:
        create_info = data
    try:
        revision = len(FullHistory.objects.filter(content_type=objname,
                       object_id=objid))
    except:
        revision = 0
    fh = FullHistory(
        revision=revision,
        action=action,
        content_type_id=content_type_id,
        object_id=objid,
        data=data,
        request=fullrequest,
        site_id=1,
        info=create_info,
    )
    fh.save()


def create_infos(requestparam, action):
    '''
        Generates a summary description of this history entry
        '''
    user_name = u'(System)'
    if requestparam:
        user_name = requestparam.user

    ret = {'I': u'%s Created', 'U': u'%s Updated',
           'D': u'%s Deleted'}[action] % user_name
    return ret
