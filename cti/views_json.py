from django.http import Http404, JsonResponse
from django.contrib import auth
from django.core import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from copy import copy
from .forms import FaultForm
from .backends import InvbookBackend
from .models import Fault, Object, User, Counter
from .helper import compare_two_faults, get_faults_from_session, post_faults_to_session,\
    make_list_of_watchers, make_string_of_watchers, send_email
import datetime


def login(request):
    result = {'login_status': False,
              'username': '',
              'error_message': ''}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                result['login_status'] = True
                result['username'] = username

                auth.login(request, user)

                date = datetime.date.today()

                try:
                    counter = Counter.objects.get(date=date)

                    counter.users += 1
                    counter.save()
                except Counter.DoesNotExist:
                    counter = Counter(date=date, users=1)

                    counter.save()
            else:
                result['error_message'] = 'your account has been disabled'
        else:
            result['error_message'] = 'invalid login or password'

    return JsonResponse(result)


@login_required
def logout(request):
    auth.logout(request)

    result = {'login_status': False}

    return JsonResponse(result)


@login_required
def index(request):
    faults = Fault.objects.filter(is_visible=True, status__in=[0, 1]).order_by('-created_at')

    post_faults_to_session(request, faults)

    result = {'faults': serializers.serialize('json', faults)}

    return JsonResponse(result)


@login_required
def my_faults(request):
    faults = Fault.objects.filter(is_visible=True, issuer=request.user.username).order_by('-created_at')

    post_faults_to_session(request, faults)

    result = {'faults': serializers.serialize('json', faults)}

    return JsonResponse(result)


@login_required
def watched_faults(request):
    list_of_faults = Fault.objects.filter(is_visible=True, status__in=[0, 1, 2]).order_by('-created_at')

    list_of_watched_faults = []

    for fault in list_of_faults:
        if request.user.username in make_list_of_watchers(fault.watchers):
            list_of_watched_faults.append(fault)

    post_faults_to_session(request, list_of_watched_faults)

    result = {'faults': serializers.serialize('json', list_of_watched_faults)}

    return JsonResponse(result)


@login_required
def resolved_faults(request):
    faults = Fault.objects.filter(is_visible=True, status=2).order_by('-created_at')

    post_faults_to_session(request, faults)

    result = {'faults': serializers.serialize('json', faults)}

    return JsonResponse(result)


@login_required
def sorted_faults(request, order_by):
    faults = get_faults_from_session(request).order_by(order_by)

    post_faults_to_session(request, faults)

    result = {'faults': serializers.serialize('json', faults)}

    return JsonResponse(result)


@login_required
def searched_faults(request):
    query = request.GET.get('searched_text')

    if query:
        faults = Fault.objects.filter(is_visible=True, status__in=[0, 1, 2]).\
            filter(Q(topic__icontains=query)).order_by('-created_at')
    else:
        faults = Fault.objects.filter(is_visible=True, status__in=[0, 1, 2]).order_by('-created_at')

    post_faults_to_session(request, faults)

    result = {'faults': serializers.serialize('json', faults)}

    return JsonResponse(result)


@login_required
def add_fault(request):
    result = {'add_fault_status': False}

    if request.method == "POST":
        form = FaultForm(request.POST)

        if form.is_valid():
            fault = form.save(commit=False)

            fault.issuer = request.user
            fault.save()

            date = datetime.date.today()

            try:
                counter = Counter.objects.get(date=date)

                counter.faults += 1
                counter.save()
            except Counter.DoesNotExist:
                counter = Counter(date=date, faults=1)

                counter.save()

            invbook = InvbookBackend()

            fault_object = invbook.get_or_create_object(fault.object_number)

            subject = 'new fault created - {} - {}'.format(fault.id, fault.topic)
            message = 'issuer: {}\n' \
                      'object: {} located in room: {}\n\n' \
                      'priority: {}\n' \
                      'topic: {}\n' \
                      'description: {}\n\n' \
                      'link to details: http://212.191.92.101:6009/admin/fault_details/{}/'. \
                format(fault.issuer, fault.object_number, fault_object.room, fault.priority,
                       fault.topic, fault.description, fault.id)

            users = User.objects.filter(is_staff=True)

            send_email(subject, message, users)

            result['add_fault_status'] = True

    return JsonResponse(result)


@login_required
def edit_fault(request, fault_id):
    result = {'edit_fault_status': False}

    try:
        fault = Fault.objects.get(pk=fault_id)

        previous_version_of_fault = copy(fault)

        if fault.issuer == request.user.username:
            if fault.status != 2 and fault.status != 3:
                form = FaultForm(request.POST or None, instance=fault)

                if request.method == "POST":
                    if form.is_valid():
                        fault = form.save(commit=False)
                        fault.save()

                        compare_two_faults(request, previous_version_of_fault, fault)

                        result['edit_fault_status'] = True

                return JsonResponse(result)
            else:
                raise Http404("this fault is already ended")
        else:
            raise Http404("you are not owner of this fault")
    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
def watch_fault(request, fault_id):
    result = {'watch_status': False}

    try:
        fault = Fault.objects.get(pk=fault_id)

        if fault.status != 3:
            watchers = make_list_of_watchers(fault.watchers)

            if request.user.username in watchers:
                watchers.remove(request.user.username)

                result['watch_status'] = False
            else:
                watchers.append(request.user.username)

                result['watch_status'] = True

            fault.watchers = make_string_of_watchers(watchers)
            fault.save()

            return JsonResponse(result)
        else:
            raise Http404("this fault is already deleted")
    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
def fault_details(fault_id):
    try:
        fault = Fault.objects.filter(pk=fault_id)

        if fault.status != 3:
            result = {'fault': serializers.serialize('json', fault)}

            return JsonResponse(result)
        else:
            raise Http404("this fault is already deleted")
    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
def object_details(object_id):
    try:
        fault_object = Object.objects.filter(object_number=object_id)

        result = {'object': serializers.serialize('json', fault_object)}

        return JsonResponse(result)
    except Object.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
def user_details(request, user_id):
    try:
        user = User.objects.get(id=user_id)

        if user.id == request.user.id:
            result = {'user': serializers.serialize('json', user)}

            return JsonResponse(result)
        else:
            raise Http404("this is not you")
    except User.DoesNotExist:
        raise Http404("user does not exist")
