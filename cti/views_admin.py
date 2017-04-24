from django.template import loader
from django.http import HttpResponse
from .models import Fault, Object
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
from django.core.mail import send_mail
from copy import copy
from .helper import compare_two_faults


@login_required
@staff_member_required
def index(request):
    template = loader.get_template('cti/admin/index.html')

    faults = Fault.objects.filter(is_visible=True, status__in=[0, 1])

    context = {'faults': faults,
               'header': 'all faults'}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def my_faults(request):
    template = loader.get_template('cti/admin/index.html')

    faults = Fault.objects.filter(is_visible=True, handler=request.user.username)

    context = {'faults': faults,
               'header': 'faults assigned to me'}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def resolved_faults(request):
    template = loader.get_template('cti/admin/index.html')

    faults = Fault.objects.filter(is_visible=True, status=2)

    context = {'faults': faults,
               'header': 'resolved faults'}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def deleted_faults(request):
    template = loader.get_template('cti/admin/index.html')

    faults = Fault.objects.filter(is_visible=False, status=3)

    context = {'faults': faults,
               'header': 'deleted faults'}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def all_users(request):
    template = loader.get_template('cti/admin/users.html')

    users = User.objects.all()

    context = {'users': users,
               'header': 'all users'}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def edit_fault(request, fault_id):
    try:
        fault = Fault.objects.get(pk=fault_id)
        previous_version_of_fault = copy(fault)

        if fault.status != 2 and fault.status != 3:
            template = loader.get_template('cti/admin/fault_form.html')

            form = AdminFaultForm(request.POST or None, instance=fault)

            if request.method == "POST":
                if form.is_valid():
                    fault = form.save(commit=False)
                    fault.save()

                    compare_two_faults(request, previous_version_of_fault, fault)

                    if request.user.username != fault.issuer:
                        subject = 'fault {} - fault was edited by admins'.format(fault.id)
                        message = 'link to details: http://212.191.92.101:6009/fault_details/{}/'. \
                            format(fault.id)
                        from_email = 'redlicki.grzegorz@gmail.com'

                        user = User.objects.get(username=fault.issuer)
                        recipient_list = [user.email]

                        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                    messages.success(request, "fault edited successful")

                    return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
                else:
                    for field in form:
                        for error in field.errors:
                            messages.warning(request, "{} - {}".format(field.name, error))

            context = {'form': form,
                       'button': 'edit',
                       'header': 'edit fault'}

            return HttpResponse(template.render(context, request))
        else:
            messages.warning(request, "this fault is already ended")

            return HttpResponseRedirect(reverse('cti:index_admin'))
    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


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
                    subject = 'fault {} - your fault was finished'.format(fault.id)
                    message = 'link to details: http://212.191.92.101:6009/fault_details/{}/'. \
                        format(fault.id)
                    from_email = 'redlicki.grzegorz@gmail.com'

                    user = User.objects.get(username=fault.issuer)
                    recipient_list = [user.email]

                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                messages.success(request, "fault finished successful")

                return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
            else:
                messages.warning(request, "you are not handler of this fault")
        else:
            messages.warning(request, "fault is not ready to finish")

        return HttpResponseRedirect(reverse('cti:index_admin'))
    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


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
                    subject = 'fault {} - your fault was deleted'.format(fault.id)
                    message = 'link to details: http://212.191.92.101:6009/fault_details/{}/'. \
                        format(fault.id)
                    from_email = 'redlicki.grzegorz@gmail.com'

                    user = User.objects.get(username=fault.issuer)
                    recipient_list = [user.email]

                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                messages.success(request, "fault deleted successful")

                return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
            else:
                messages.warning(request, "you are not handler of this fault")
        else:
            messages.warning(request, "fault is already deleted")

        return HttpResponseRedirect(reverse('cti:index_admin'))
    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


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
                    subject = 'fault {} - your fault was assigned'.format(fault.id)
                    message = 'link to details: http://212.191.92.101:6009/fault_details/{}/'. \
                        format(fault.id)
                    from_email = 'redlicki.grzegorz@gmail.com'

                    user = User.objects.get(username=fault.issuer)
                    recipient_list = [user.email]

                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                messages.success(request, "fault assigned successful")

                return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
            else:
                messages.warning(request, "fault status is not free to assign")
        else:
            messages.warning(request, "fault is already assigned")

        return HttpResponseRedirect(reverse('cti:index_admin'))
    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


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

                subject = 'fault {} - fault was reasigned'.format(fault.id)
                message = 'link to details: http://212.191.92.101:6009/admin/fault_details/{}/'. \
                    format(fault.id)
                from_email = 'redlicki.grzegorz@gmail.com'

                issuer = User.objects.get(username=fault.issuer)

                recipient_list = [user.email, issuer.email]

                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                messages.success(request, "fault reassigned successful")

                return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
            else:
                messages.warning(request, "this user is not authorized to assigning faults")
        else:
            messages.warning(request, "you can not reassign this fault")

        return HttpResponseRedirect(reverse('cti:index_admin'))
    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


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
                    subject = 'fault {} - your fault was restored'.format(fault.id)
                    message = 'link to details: http://212.191.92.101:6009/fault_details/{}/'. \
                        format(fault.id)
                    from_email = 'redlicki.grzegorz@gmail.com'

                    user = User.objects.get(username=fault.issuer)
                    recipient_list = [user.email]

                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                messages.success(request, "fault restore successful")

                return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
            else:
                messages.warning(request, "you are not handler of this fault")
        else:
            messages.warning(request, "fault is not ended")

        return HttpResponseRedirect(reverse('cti:index_admin'))
    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


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

                    messages.success(request, "user edited successful")

                    return HttpResponseRedirect(reverse('cti:user_details_admin', kwargs={'user_id': user_id}))
                else:
                    for field in form:
                        for error in field.errors:
                            messages.warning(request, "{} - {}".format(field.name, error))

            context = {'form': form,
                       'button': 'edit',
                       'header': 'edit user'}

            return HttpResponse(template.render(context, request))
        else:
            messages.warning(request, "this user is not editable")

            return HttpResponseRedirect(reverse('cti:all_users_admin'))
    except User.DoesNotExist:
        raise Http404("user does not exist")


@login_required
@staff_member_required
def block_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)

        if user.is_active:
            if not user.is_staff:
                user.is_active = False
                user.save()

                messages.success(request, "user blocked successful")

                return HttpResponseRedirect(reverse('cti:user_details_admin', kwargs={'user_id': user_id}))
            else:
                messages.warning(request, "user is one of admins")
        else:
            messages.warning(request, "user is already blocked")

        return HttpResponseRedirect(reverse('cti:all_users_admin'))
    except User.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
@staff_member_required
def restore_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)

        if not user.is_active:
            if not user.is_staff:
                user.is_active = True
                user.save()

                messages.success(request, "user restored successful")

                return HttpResponseRedirect(reverse('cti:user_details_admin', kwargs={'user_id': user_id}))
            else:
                messages.warning(request, "user is one of admins")
        else:
            messages.warning(request, "user is not blocked")

        return HttpResponseRedirect(reverse('cti:all_users_admin'))
    except User.DoesNotExist:
        raise Http404("fault does not exist")


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

                messages.success(request, 'password has been changed')

                return HttpResponseRedirect(reverse('cti:user_details_admin', kwargs={'user_id': request.user.id}))
            else:
                messages.warning(request, 'password fields are different!')
        else:
            messages.warning(request, 'old password is wrong')

    context = {'button': 'change',
               'header': 'change password'}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def fault_details(request, fault_id):
    template = loader.get_template('cti/admin/fault_details.html')

    try:
        fault = Fault.objects.get(pk=fault_id)

        context = {'fault': fault,
                   'header': 'fault\'s details'}

        return HttpResponse(template.render(context, request))
    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
@staff_member_required
def object_details(request, object_id):
    template = loader.get_template('cti/admin/object_details.html')

    try:
        fault_object = Object.objects.get(object_number=object_id)

        context = {'object': fault_object,
                   'header': 'object\'s details'}

        return HttpResponse(template.render(context, request))
    except Object.DoesNotExist:
        raise Http404("object does not exist")


@login_required
@staff_member_required
def user_details(request, user_id):
    template = loader.get_template('cti/admin/user_details.html')

    try:
        user = User.objects.get(id=user_id)

        context = {'user': user,
                   'header': 'user\'s details'}

        return HttpResponse(template.render(context, request))
    except User.DoesNotExist:
        raise Http404("user does not exist")


@login_required
@staff_member_required
def ask_for_reassign(request, fault_id, username):
    try:
        fault = Fault.objects.get(pk=fault_id)

        if request.user.is_staff:
            subject = 'fault {} - asking for reasign'.format(fault.id)
            message = 'please reassign me to this fault\n\n' \
                      'link to reassign automatically: ' \
                      'http://212.191.92.101:6009/admin/fault_details/{}/reassign_fault/{}'. \
                format(fault.id, username)
            from_email = 'redlicki.grzegorz@gmail.com'

            user = User.objects.get(username=fault.handler)
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            messages.success(request, "ask for reassign send successfully")

            return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
        else:
            messages.warning(request, "you are not allowed to reassigning")

            return HttpResponseRedirect(reverse('cti:index_admin'))
    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
@staff_member_required
def report_phone_number(request, fault_id):
    try:
        fault = Fault.objects.get(pk=fault_id)

        if request.user.is_staff:
            subject = 'fault {} - phone number reported'.format(fault.id)
            message = 'please change phone number\n' \
                      '{} - this is not working\n\n' \
                      'link to details: http://212.191.92.101:6009/fault_details/{}/'. \
                format(fault.phone_number, fault.topic, fault.description, fault.id)
            from_email = 'redlicki.grzegorz@gmail.com'

            user = User.objects.get(username=fault.issuer)
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            messages.success(request, "phone number reported successfully")

            return HttpResponseRedirect(reverse('cti:fault_details_admin', kwargs={'fault_id': fault_id}))
        else:
            messages.warning(request, "you are not allowed to reporting phones")

            return HttpResponseRedirect(reverse('cti:index_admin'))
    except Fault.DoesNotExist:
        raise Http404("fault does not exist")
