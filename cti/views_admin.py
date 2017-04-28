from django.template import loader
from django.http import HttpResponse
from .models import Fault, Object, History
from django.http import Http404
from .forms import AdminFaultForm, UserForm
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import User
from copy import copy
from .helper import compare_two_faults, make_string_of_watchers, make_list_of_watchers, send_email
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


@login_required
@staff_member_required
def index(request):
    template = loader.get_template('cti/admin/index.html')

    faults = Fault.objects.filter(is_visible=True, status__in=[0, 1])

    context = {'faults': faults,
               'all_faults': Fault.objects.all(),
               'header': _('all faults')}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def my_faults(request):
    template = loader.get_template('cti/admin/index.html')

    faults = Fault.objects.filter(is_visible=True, handler=request.user.username)

    context = {'faults': faults,
               'all_faults': Fault.objects.all(),
               'header': _('faults assigned to me')}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def watched_faults(request):
    template = loader.get_template('cti/admin/index.html')

    all_faults = Fault.objects.filter(is_visible=True, status__in=[0, 1])
    faults = []

    for fault in all_faults:
        if request.user.username in make_list_of_watchers(fault.watchers):
            faults.append(fault)

    context = {'faults': faults,
               'all_faults': Fault.objects.all(),
               'header': _('watched faults')}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def resolved_faults(request):
    template = loader.get_template('cti/admin/index.html')

    faults = Fault.objects.filter(is_visible=True, status=2)

    context = {'faults': faults,
               'all_faults': Fault.objects.all(),
               'header': _('resolved faults')}

    return HttpResponse(template.render(context, request))


@login_required
def searched_faults(request):
    template = loader.get_template('cti/admin/index.html')

    query = request.GET.get('searched_text')

    if query:
        faults = Fault.objects.filter(Q(topic__icontains=query))
    else:
        messages.warning(request, _('no matches for this query'))

        faults = Fault.objects.all()

    context = {'faults': faults,
               'all_faults': Fault.objects.all(),
               'header': _('searched faults')}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def deleted_faults(request):
    template = loader.get_template('cti/admin/index.html')

    faults = Fault.objects.filter(is_visible=False, status=3)

    context = {'faults': faults,
               'all_faults': Fault.objects.all(),
               'header': _('deleted faults')}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def all_users(request):
    template = loader.get_template('cti/admin/users.html')

    users = User.objects.all()

    context = {'all_faults': Fault.objects.all(),
               'users': users,
               'header': _('all users')}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def all_history(request):
    template = loader.get_template('cti/admin/history.html')

    history = History.objects.all()

    context = {'all_faults': Fault.objects.all(),
               'history': history,
               'header': _('history')}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def edit_fault(request, fault_id):
    try:
        fault = Fault.objects.get(pk=fault_id)
        previous_version_of_fault = copy(fault)

        if fault.handler == request.user.username:
            if fault.status != 2 and fault.status != 3:
                template = loader.get_template('cti/admin/fault_form.html')

                form = AdminFaultForm(request.POST or None, instance=fault)

                if request.method == "POST":
                    if form.is_valid():
                        fault = form.save(commit=False)
                        fault.save()

                        compare_two_faults(request, previous_version_of_fault, fault)

                        if request.user.username != fault.issuer:
                            subject = 'your fault - {} - has been edited by admins'.format(fault.id)
                            message = 'priority: {}\n' \
                                      'topic: {}\n' \
                                      'description: {}\n\n' \
                                      'link to details: http://212.191.92.101:6009/fault_details/{}/'. \
                                format(fault.priority, fault.topic, fault.description, fault.id)

                            users = User.objects.filter(username=fault.issuer)

                            send_email(subject, message, users)

                        messages.success(request, _("fault edited successful"))

                        return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
                    else:
                        for field in form:
                            for error in field.errors:
                                messages.warning(request, "{} - {}".format(field.name, error))

                context = {'all_faults': Fault.objects.all(),
                           'form': form,
                           'button': _('edit'),
                           'header': _('edit fault')}

                return HttpResponse(template.render(context, request))
            else:
                messages.warning(request, _("this fault is already ended"))
        else:
            messages.warning(request, _("you are not handler of this fault"))

        return HttpResponseRedirect(reverse('cti:index_admin'))
    except Fault.DoesNotExist:
        raise Http404(_("fault does not exist"))


@login_required
@staff_member_required
def watch_fault(request, fault_id):
    try:
        fault = Fault.objects.get(pk=fault_id)

        if fault.status != 2 and fault.status != 3:
            watchers = make_list_of_watchers(fault.watchers)

            if request.user.username in watchers:
                watchers.remove(request.user.username)

                messages.success(request, _("you don't watch on this fault from this time"))
            else:
                watchers.append(request.user.username)

                messages.success(request, _("you watch on this fault from this time"))

            fault.watchers = make_string_of_watchers(watchers)
            fault.save()
        else:
            messages.warning(request, _("this fault is already ended"))

        return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
    except Fault.DoesNotExist:
        raise Http404(_("fault does not exist"))


@login_required
@staff_member_required
def finish_fault(request, fault_id):
    try:
        fault = Fault.objects.get(pk=fault_id)
        previous_version_of_fault = copy(fault)

        if fault.status != 2 and fault.status != 3:
            if fault.handler == request.user.username:
                fault.status = 2
                fault.save()

                compare_two_faults(request, previous_version_of_fault, fault)

                if request.user.username != fault.issuer:
                    subject = 'your fault - {} - has been finished already'.format(fault.id)
                    message = 'priority: {}\n' \
                              'topic: {}\n' \
                              'description: {}\n\n' \
                              'link to details: http://212.191.92.101:6009/fault_details/{}/'. \
                        format(fault.priority, fault.topic, fault.description, fault.id)

                    users = User.objects.filter(username=fault.issuer)

                    send_email(subject, message, users)

                messages.success(request, _("fault finished successful"))

                return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
            else:
                messages.warning(request, _("you are not handler of this fault"))
        else:
            messages.warning(request, _("fault is not ready to finish"))

        return HttpResponseRedirect(reverse('cti:index_admin'))
    except Fault.DoesNotExist:
        raise Http404(_("fault does not exist"))


@login_required
@staff_member_required
def delete_fault(request, fault_id):
    try:
        fault = Fault.objects.get(pk=fault_id)
        previous_version_of_fault = copy(fault)

        if fault.is_visible:
            if fault.handler == request.user.username:
                fault.is_visible = False
                fault.status = 3
                fault.save()

                compare_two_faults(request, previous_version_of_fault, fault)

                if request.user.username != fault.issuer:
                    subject = 'your fault - {} - has been deleted already'.format(fault.id)
                    message = 'priority: {}\n' \
                              'topic: {}\n' \
                              'description: {}\n\n'. \
                        format(fault.priority, fault.topic, fault.description)

                    users = User.objects.filter(username=fault.issuer)

                    send_email(subject, message, users)

                messages.success(request, _("fault deleted successful"))

                return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
            else:
                messages.warning(request, _("you are not handler of this fault"))
        else:
            messages.warning(request, _("fault is already deleted"))

        return HttpResponseRedirect(reverse('cti:index_admin'))
    except Fault.DoesNotExist:
        raise Http404(_("fault does not exist"))


@login_required
@staff_member_required
def assign_to_me(request, fault_id):
    try:
        fault = Fault.objects.get(pk=fault_id)
        previous_version_of_fault = copy(fault)

        if fault.handler == '0':
            if fault.status == 0:
                fault.handler = request.user.get_username()
                fault.status = 1
                fault.save()

                compare_two_faults(request, previous_version_of_fault, fault)

                if request.user.username != fault.issuer:
                    subject = 'your fault - {} - has been started already'.format(fault.id)
                    message = 'priority: {}\n' \
                              'topic: {}\n' \
                              'description: {}\n\n' \
                              'link to details: http://212.191.92.101:6009/fault_details/{}/'. \
                        format(fault.priority, fault.topic, fault.description, fault.id)

                    users = User.objects.filter(username=fault.issuer)

                    send_email(subject, message, users)

                messages.success(request, _("fault assigned successful"))

                return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
            else:
                messages.warning(request, _("fault status is not free to assign"))
        else:
            messages.warning(request, _("fault is already assigned"))

        return HttpResponseRedirect(reverse('cti:index_admin'))
    except Fault.DoesNotExist:
        raise Http404(_("fault does not exist"))


@login_required
@staff_member_required
def reassign_fault(request, fault_id, username):
    try:
        fault = Fault.objects.get(pk=fault_id)
        previous_version_of_fault = copy(fault)

        if fault.handler == request.user.username:
            user = User.objects.get(username=username)

            if user.is_staff:
                fault.handler = username
                fault.save()

                compare_two_faults(request, previous_version_of_fault, fault)

                messages.success(request, _("fault reassigned successful"))

                return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
            else:
                messages.warning(request, _("this user is not authorized to assigning faults"))
        else:
            messages.warning(request, _("you can not reassign this fault"))

        return HttpResponseRedirect(reverse('cti:index_admin'))
    except Fault.DoesNotExist:
        raise Http404(_("fault does not exist"))


@login_required
@staff_member_required
def restore_fault(request, fault_id):
    try:
        fault = Fault.objects.get(pk=fault_id)
        previous_version_of_fault = copy(fault)

        if fault.status == 2 or fault.status == 3:
            if fault.handler == request.user.username:
                fault.is_visible = True
                fault.status = 1
                fault.save()

                compare_two_faults(request, previous_version_of_fault, fault)

                if request.user.username != fault.issuer:
                    subject = 'your fault - {} - has been restore already'.format(fault.id)
                    message = 'priority: {}\n' \
                              'topic: {}\n' \
                              'description: {}\n\n' \
                              'link to details: http://212.191.92.101:6009/fault_details/{}/'. \
                        format(fault.priority, fault.topic, fault.description, fault.id)

                    users = User.objects.filter(username=fault.issuer)

                    send_email(subject, message, users)

                messages.success(request, _("fault restore successful"))

                return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
            else:
                messages.warning(request, _("you are not handler of this fault"))
        else:
            messages.warning(request, _("fault is not ended"))

        return HttpResponseRedirect(reverse('cti:index_admin'))
    except Fault.DoesNotExist:
        raise Http404(_("fault does not exist"))


@login_required
@staff_member_required
def edit_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)

        if not user.is_staff or user.username == request.user.username:
            template = loader.get_template('cti/admin/user_form.html')

            form = UserForm(request.POST or None, instance=user)

            if request.method == "POST":
                if form.is_valid():
                    user = form.save(commit=False)
                    user.save()

                    messages.success(request, _("user edited successful"))

                    return HttpResponseRedirect(reverse('cti:user_details_admin', kwargs={'user_id': user_id}))
                else:
                    for field in form:
                        for error in field.errors:
                            messages.warning(request, "{} - {}".format(field.name, error))

            context = {'all_faults': Fault.objects.all(),
                       'form': form,
                       'button': _('edit'),
                       'header': _('edit user')}

            return HttpResponse(template.render(context, request))
        else:
            messages.warning(request, _("this user is not editable"))

            return HttpResponseRedirect(reverse('cti:all_users_admin'))
    except User.DoesNotExist:
        raise Http404(_("user does not exist"))


@login_required
@staff_member_required
def block_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)

        if user.is_active:
            if not user.is_staff:
                user.is_active = False
                user.save()

                subject = 'support center blocked your account'
                message = 'Hello,\n\n' \
                          'your account on support center has been blocked already\n' \
                          'Please, contact with admins of CTI building to resolve this case.\n\n' \
                          'BR,\n' \
                          'support center admins'

                users = User.objects.filter(id=user_id)

                send_email(subject, message, users)

                messages.success(request, _("user blocked successful"))

                return HttpResponseRedirect(reverse('cti:user_details_admin', kwargs={'user_id': user_id}))
            else:
                messages.warning(request, _("user is one of admins"))
        else:
            messages.warning(request, _("user is already blocked"))

        return HttpResponseRedirect(reverse('cti:all_users_admin'))
    except User.DoesNotExist:
        raise Http404(_("fault does not exist"))


@login_required
@staff_member_required
def restore_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)

        if not user.is_active:
            if not user.is_staff:
                user.is_active = True
                user.save()

                subject = 'support center restore your account'
                message = 'Hello,\n\n' \
                          'your account on support center has been restore already\n' \
                          'You have all previous privileges.\n\n' \
                          'BR,\n' \
                          'support center admins'

                users = User.objects.filter(id=user_id)

                send_email(subject, message, users)

                messages.success(request, _("user restored successful"))

                return HttpResponseRedirect(reverse('cti:user_details_admin', kwargs={'user_id': user_id}))
            else:
                messages.warning(request, _("user is one of admins"))
        else:
            messages.warning(request, _("user is not blocked"))

        return HttpResponseRedirect(reverse('cti:all_users_admin'))
    except User.DoesNotExist:
        raise Http404(_("fault does not exist"))


@login_required
@staff_member_required
def change_password(request):
    template = loader.get_template('cti/admin/change_password.html')

    if request.method == "POST":
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        new_password_repeat = request.POST['new_password_repeat']

        user = User.objects.get(username__exact=request.user)

        if user.check_password(old_password):
            if new_password == new_password_repeat:
                user.set_password(new_password)
                user.save()

                user = authenticate(username=request.user, password=new_password)
                auth.login(request, user)

                messages.success(request, _('password has been changed'))

                return HttpResponseRedirect(reverse('cti:user_details_admin', kwargs={'user_id': request.user.id}))
            else:
                messages.warning(request, _('password fields are different!'))
        else:
            messages.warning(request, _('old password is wrong'))

    context = {'all_faults': Fault.objects.all(),
               'button': _('change'),
               'header': _('change password')}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def fault_details(request, fault_id):
    template = loader.get_template('cti/admin/fault_details.html')

    try:
        fault = Fault.objects.get(pk=fault_id)
        history = History.objects.filter(fault_id=fault_id)

        watchers = make_list_of_watchers(fault.watchers)

        if request.user.username in watchers:
            watcher = True
        else:
            watcher = False

        context = {'fault': fault,
                   'all_faults': Fault.objects.all(),
                   'watcher': watcher,
                   'history': history,
                   'header': _('fault\'s details')}

        return HttpResponse(template.render(context, request))
    except Fault.DoesNotExist:
        raise Http404(_("fault does not exist"))


@login_required
@staff_member_required
def object_details(request, object_id):
    template = loader.get_template('cti/admin/object_details.html')

    try:
        fault_object = Object.objects.get(object_number=object_id)

        context = {'all_faults': Fault.objects.all(),
                   'object': fault_object,
                   'header': _('object\'s details')}

        return HttpResponse(template.render(context, request))
    except Object.DoesNotExist:
        raise Http404(_("object does not exist"))


@login_required
@staff_member_required
def user_details(request, user_id):
    template = loader.get_template('cti/admin/user_details.html')

    try:
        user = User.objects.get(id=user_id)

        context = {'all_faults': Fault.objects.all(),
                   'user': user,
                   'header': _('user\'s details')}

        return HttpResponse(template.render(context, request))
    except User.DoesNotExist:
        raise Http404(_("user does not exist"))


@login_required
@staff_member_required
def ask_for_reassign(request, fault_id, username):
    try:
        fault = Fault.objects.get(pk=fault_id)

        if request.user.is_staff:
            if fault.handler != request.user.username:
                subject = 'fault - {} - ask for reassign'.format(fault.id)
                message = 'ask for reassign has been sent by {}\n\n' \
                          'priority: {}\n' \
                          'topic: {}\n' \
                          'description: {}\n\n' \
                          'link to do this automatically: ' \
                          'http://212.191.92.101:6009/admin/fault_details/{}/reassign_fault/{}'. \
                    format(username, fault.priority, fault.topic, fault.description, fault.id, username)

                users = User.objects.filter(username=fault.handler)

                send_email(subject, message, users)

                messages.success(request, _("ask for reassign send successfully"))

                return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
            else:
                messages.warning(request, _("you are handler of this fault already"))
        else:
            messages.warning(request, _("you are not allowed to reassigning"))

        return HttpResponseRedirect(reverse('cti:index_admin'))
    except Fault.DoesNotExist:
        raise Http404(_("fault does not exist"))


@login_required
@staff_member_required
def report_phone_number(request, fault_id):
    try:
        fault = Fault.objects.get(pk=fault_id)

        if request.user.is_staff:
            if request.user.username != fault.issuer:
                subject = 'fault - {} - your phone has been reported'.format(fault.id)
                message = 'your phone number has been repored\n\n' \
                          'priority: {}\n' \
                          'topic: {}\n' \
                          'description: {}\n\n' \
                          'link to details: http://212.191.92.101:6009/fault_details/{}/'. \
                    format(fault.priority, fault.topic, fault.description, fault.id)

                users = User.objects.filter(username=fault.handler)

                send_email(subject, message, users)

                messages.success(request, _("phone number reported successfully"))

                return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
            else:
                messages.warning(request, _("you are issuer of this fault"))
        else:
            messages.warning(request, _("you are not allowed to reporting phones"))

            return HttpResponseRedirect(reverse('cti:index_admin'))
    except Fault.DoesNotExist:
        raise Http404(_("fault does not exist"))
