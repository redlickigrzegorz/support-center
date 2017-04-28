from django.template import loader
from django.http import HttpResponse
from .models import Fault, Object, User
from django.http import Http404
from .forms import FaultForm
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .backends import InvbookBackend
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from copy import copy
from .helper import compare_two_faults, get_faults_from_session, post_faults_to_session,\
    make_list_of_watchers, make_string_of_watchers, send_email
from django.utils.translation import ugettext_lazy as _


def login(request):
    template = loader.get_template('cti/client/login.html')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)

                if user.is_staff:
                    return HttpResponseRedirect(reverse('cti:index_admin'))
                else:
                    return HttpResponseRedirect(reverse('cti:index'))
            else:
                messages.warning(request, _('your account has been disabled'))
        else:
            messages.error(request, _('invalid login or password'))

    return HttpResponse(template.render(request=request))


def logout(request):
    template = loader.get_template('cti/client/logout.html')

    auth.logout(request)

    return HttpResponse(template.render(request=request))


@login_required
def index(request):
    template = loader.get_template('cti/client/index.html')

    faults_list = Fault.objects.filter(is_visible=True, status__in=[0, 1]).order_by('-created_at')
    post_faults_to_session(request, faults_list)

    paginator = Paginator(faults_list, 5)

    page = request.GET.get('page')

    try:
        faults = paginator.page(page)
    except PageNotAnInteger:
        faults = paginator.page(1)
    except EmptyPage:
        faults = paginator.page(paginator.num_pages)

    context = {'faults': faults,
               'all_faults': Fault.objects.filter(is_visible=True, status__in=[0, 1, 2]),
               'header': _('all faults')}

    return HttpResponse(template.render(context, request))


@login_required
def my_faults(request):
    template = loader.get_template('cti/client/index.html')

    faults_list = Fault.objects.filter(is_visible=True, issuer=request.user.get_username()).order_by('-created_at')
    post_faults_to_session(request, faults_list)

    paginator = Paginator(faults_list, 5)

    page = request.GET.get('page')

    try:
        faults = paginator.page(page)
    except PageNotAnInteger:
        faults = paginator.page(1)
    except EmptyPage:
        faults = paginator.page(paginator.num_pages)

    context = {'faults': faults,
               'all_faults': Fault.objects.filter(is_visible=True, status__in=[0, 1, 2]),
               'header': _('my faults')}

    return HttpResponse(template.render(context, request))


@login_required
def watched_faults(request):
    template = loader.get_template('cti/client/index.html')

    all_faults = Fault.objects.filter(is_visible=True, status__in=[0, 1]).order_by('-created_at')
    faults_list = []

    for fault in all_faults:
        if request.user.username in make_list_of_watchers(fault.watchers):
            faults_list.append(fault)

    post_faults_to_session(request, faults_list)

    paginator = Paginator(faults_list, 5)

    page = request.GET.get('page')

    try:
        faults = paginator.page(page)
    except PageNotAnInteger:
        faults = paginator.page(1)
    except EmptyPage:
        faults = paginator.page(paginator.num_pages)

    context = {'faults': faults,
               'all_faults': Fault.objects.filter(is_visible=True, status__in=[0, 1, 2]),
               'header': _('watched faults')}

    return HttpResponse(template.render(context, request))


@login_required
def resolved_faults(request):
    template = loader.get_template('cti/client/index.html')

    faults_list = Fault.objects.filter(is_visible=True, status=2).order_by('-created_at')
    post_faults_to_session(request, faults_list)

    paginator = Paginator(faults_list, 5)

    page = request.GET.get('page')

    try:
        faults = paginator.page(page)
    except PageNotAnInteger:
        faults = paginator.page(1)
    except EmptyPage:
        faults = paginator.page(paginator.num_pages)

    context = {'faults': faults,
               'all_faults': Fault.objects.filter(is_visible=True, status__in=[0, 1, 2]),
               'header': _('resolved faults')}

    return HttpResponse(template.render(context, request))


@login_required
def sorted_faults(request, order_by):
    template = loader.get_template('cti/client/index.html')

    faults_list = get_faults_from_session(request).order_by(order_by)
    post_faults_to_session(request, faults_list)

    paginator = Paginator(faults_list, 5)

    page = request.GET.get('page')

    try:
        faults = paginator.page(page)
    except PageNotAnInteger:
        faults = paginator.page(1)
    except EmptyPage:
        faults = paginator.page(paginator.num_pages)

    context = {'faults': faults,
               'all_faults': Fault.objects.filter(is_visible=True, status__in=[0, 1, 2]),
               'header': _('sorted faults')}

    return HttpResponse(template.render(context, request))


@login_required
def searched_faults(request):
    template = loader.get_template('cti/client/index.html')

    query = request.GET.get('searched_text')

    if query:
        faults_list = Fault.objects.filter(is_visible=True, status__in=[0, 1, 2]).\
            filter(Q(topic__icontains=query)).order_by('-created_at')
    else:
        messages.warning(request, _('no matches for this query'))

        faults_list = Fault.objects.filter(is_visible=True, status__in=[0, 1, 2]).order_by('-created_at')

    post_faults_to_session(request, faults_list)

    paginator = Paginator(faults_list, 5)

    page = request.GET.get('page')

    try:
        faults = paginator.page(page)
    except PageNotAnInteger:
        faults = paginator.page(1)
    except EmptyPage:
        faults = paginator.page(paginator.num_pages)

    context = {'faults': faults,
               'all_faults': Fault.objects.filter(is_visible=True, status__in=[0, 1, 2]),
               'header': _('searched faults')}

    return HttpResponse(template.render(context, request))


@login_required
def add_fault(request):
    template = loader.get_template('cti/client/fault_form.html')

    if request.method == "POST":
        form = FaultForm(request.POST)

        if form.is_valid():
            fault = form.save(commit=False)
            fault.issuer = request.user
            fault.save()

            invbook = InvbookBackend()
            fault_object = invbook.get_or_create_object(fault.object_number)

            subject = 'new fault created - {} - {}'.format(fault.id, fault.topic)
            message = 'issuer: {}\n' \
                      'object: {} located in room: {}\n\n' \
                      'priority: {}\n' \
                      'topic: {}\n' \
                      'description: {}\n\n' \
                      'link to details: http://212.191.92.101:6009/admin/fault_details/{}/'.\
                format(fault.issuer, fault.object_number, fault_object.room, fault.priority,
                       fault.topic, fault.description, fault.id)

            users = User.objects.filter(is_staff=True)

            send_email(subject, message, users)

            messages.success(request, _("fault added successful"))

            return HttpResponseRedirect(reverse('cti:fault_details', kwargs={'fault_id': fault.id}))
        else:
            for field in form:
                for error in field.errors:
                    messages.warning(request, "{} - {}".format(field.name, error))
    else:
        form = FaultForm()

    context = {'all_faults': Fault.objects.filter(is_visible=True, status__in=[0, 1, 2]),
               'form': form,
               'button': _('add'),
               'header': _('new fault')}

    return HttpResponse(template.render(context, request))


@login_required
def edit_fault(request, fault_id):
    try:
        fault = Fault.objects.get(pk=fault_id)
        previous_version_of_fault = copy(fault)

        if fault.issuer == request.user.username:
            if fault.status != 2 and fault.status != 3:
                template = loader.get_template('cti/client/fault_form.html')

                form = FaultForm(request.POST or None, instance=fault)

                if request.method == "POST":
                    if form.is_valid():
                        fault = form.save(commit=False)
                        fault.save()

                        compare_two_faults(request, previous_version_of_fault, fault)

                        messages.success(request, _("fault edited successful"))

                        return HttpResponseRedirect(reverse('cti:fault_details', kwargs={'fault_id': fault_id}))
                    else:
                        for field in form:
                            for error in field.errors:
                                messages.warning(request, "{} - {}".format(field.name, error))

                context = {'all_faults': Fault.objects.filter(is_visible=True, status__in=[0, 1, 2]),
                           'form': form,
                           'button': _('edit'),
                           'header': _('edit fault')}

                return HttpResponse(template.render(context, request))
            else:
                raise Http404(_("this fault is already ended"))
        else:
            raise Http404(_("you are not owner of this fault"))
    except Fault.DoesNotExist:
        raise Http404(_("fault does not exist"))


@login_required
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

            return HttpResponseRedirect(reverse('cti:fault_details', kwargs={'fault_id': fault_id}))
        else:
            raise Http404(_("this fault is already ended"))
    except Fault.DoesNotExist:
        raise Http404(_("fault does not exist"))


@login_required
def fault_details(request, fault_id):
    template = loader.get_template('cti/client/fault_details.html')

    try:
        fault = Fault.objects.get(pk=fault_id)

        watchers = make_list_of_watchers(fault.watchers)

        if request.user.username in watchers:
            watcher = True
        else:
            watcher = False

        if not fault.status == 3:
            context = {'fault': fault,
                       'all_faults': Fault.objects.filter(is_visible=True, status__in=[0, 1, 2]),
                       'watcher': watcher,
                       'header': _('fault\'s details')}

            return HttpResponse(template.render(context, request))
        else:
            raise Http404(_("this fault is already ended"))
    except Fault.DoesNotExist:
        raise Http404(_("fault does not exist"))


@login_required
def object_details(request, object_id):
    template = loader.get_template('cti/client/object_details.html')

    try:
        fault_object = Object.objects.get(object_number=object_id)

        context = {'all_faults': Fault.objects.filter(is_visible=True, status__in=[0, 1, 2]),
                   'object': fault_object,
                   'header': _('object\'s details')}

        return HttpResponse(template.render(context, request))
    except Object.DoesNotExist:
        raise Http404(_("object does not exist"))


@login_required
def user_details(request):
    template = loader.get_template('cti/client/user_details.html')

    try:
        user = User.objects.get(username__exact=request.user)

        context = {'all_faults': Fault.objects.filter(is_visible=True, status__in=[0, 1, 2]),
                   'user': user,
                   'header': _('user\'s details')}

        return HttpResponse(template.render(context, request))
    except User.DoesNotExist:
        raise Http404(_("user does not exist"))
