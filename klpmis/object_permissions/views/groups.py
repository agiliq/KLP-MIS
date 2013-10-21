import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render

from object_permissions import get_user_perms
from object_permissions.signals import view_edit_user
from object_permissions.views.permissions import ObjectPermissionForm


@login_required
def user_permissions(request, id, user_id=None):
    """
    Ajax call to update a user's permissions

    @param id: id of Group
    """
    editor = request.user
    group = get_object_or_404(Group, id=id)

    if not (editor.is_superuser or editor.has_perm('admin', group)):
        return HttpResponseForbidden('You do not have sufficient privileges')

    if request.method == 'POST':
        form = ObjectPermissionForm(Group, request.POST)
        if form.is_valid():
            form.update_perms()
            user = form.cleaned_data['user']

            # send signal
            view_edit_user.send(sender=editor, user=user, obj=group)

            # return html to replace existing user row
            url = reverse('group-permissions', args=[id])
            context = {'object': group, 'user_detail': user, 'url': url}
            return render(request,
                          "object_permissions/muddle/group/user_row.html",
                          context)

        # error in form return ajax response
        content = json.dumps(form.errors)
        return HttpResponse(content, mimetype='application/json')

    # render a form for an existing user only
    form_user = get_object_or_404(User, id=user_id)
    data = {'permissions': get_user_perms(form_user, group),
            'obj': group, 'user': user_id}
    form = ObjectPermissionForm(Group, data)
    context = {'form': form, 'obj': group, 'user_id': user_id,
               'url': reverse('group-permissions', args=[group.id])}
    return render(request,
                  "object_permissions/permissions/form.html",
                  context)


@login_required
def all_permissions(request, id,
                    template='object_permissions/permissions/objects.html',
                    rest=False):
    """
    Generic view for displaying permissions on all objects.

    @param id: id of group
    @param template: template to render the results with, default is
    permissions/objects.html
    """
    user = request.user
    group = get_object_or_404(Group, pk=id)

    if not (user.is_superuser or group.user_set.filter(pk=user.pk).exists()):
        if not rest:
            return HttpResponseForbidden('You do not have \
                    sufficient privileges')
        else:
            return {'error': 'You do not have sufficient privileges'}

    perm_dict = group.get_all_objects_any_perms()

    # exclude group permissions from this view, they are treated special
    try:
        del perm_dict[Group]
    except KeyError:
        pass

    # XXX repack perm_dict so that class names are used as keys instead of the
    # classes.  Django templates will automatically execute anything callable
    # if you try to use it, even classes!  #5619
    repacked = {}
    for cls, objs in perm_dict.items():
        repacked[cls.__name__] = objs

    if not rest:
        context = {'persona': group, 'perm_dict': repacked}
        return render(request, template, context)
    else:
        return context
