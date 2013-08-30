from django.http import HttpResponse


def set_session(request):
    """ This method uses for set the session """

    request.session['session_sch_typ'] = request.GET.get('sessionVal')
    return HttpResponse('Success')
