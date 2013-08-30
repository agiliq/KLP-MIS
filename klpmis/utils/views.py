from django.http import HttpResponse


def KLP_Set_Session(request):
    """ This method uses for set the session """

    request.session['session_sch_typ'] = request.GET.get('sessionVal')
    return HttpResponse('Success')
