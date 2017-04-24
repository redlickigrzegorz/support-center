from .models import Fault, Object
from django.http import Http404
from .forms import FaultForm
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from .backends import InvbookBackend
from .models import User
from .views import post_faults_to_session, get_faults_from_session
from django.db.models import Q
from django.core.mail import send_mail
from .helper import compare_two_faults
from copy import copy


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
    faults = Fault.objects.filter(issuer=request.user.get_username(), is_visible=True).order_by('-created_at')
    post_faults_to_session(request, faults)

    result = {'faults': serializers.serialize('json', faults)}

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
        faults = get_faults_from_session(request).filter(Q(topic__icontains=query)).order_by('-created_at')
    else:
        faults = get_faults_from_session(request).order_by('-created_at')

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

            invbook = InvbookBackend()
            invbook.get_or_create_object(fault.object_number)

            subject = 'fault {} created - {}'.format(fault.id, fault.topic)
            message = 'issuer: {}\n' \
                      'object: {}\n\n' \
                      'topic: {}\n' \
                      'description: {}\n\n' \
                      'link to details: http://212.191.92.101:6009/admin/fault_details/{}/'. \
                format(fault.issuer, fault.object_number, fault.topic, fault.description, fault.id)
            from_email = 'redlicki.grzegorz@gmail.com'
            recipient_list = []

            users = User.objects.filter(is_staff=True)

            for user in users:
                recipient_list.append(user.email)

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

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
                raise Http404("fault {} is already ended".format(fault_id))
        else:
            raise Http404("you are not owner of fault {}".format(fault_id))
    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
def fault_details(fault_id):
    try:
        fault = Fault.objects.filter(pk=fault_id)

        if fault.status == 3:
            result = {'fault': serializers.serialize('json', fault)}

            return JsonResponse(result)
        else:
            raise Http404("fault does not exist")
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
def user_details(request):
    try:
        user = User.objects.filter(username__exact=request.user)
        result = {'user': serializers.serialize('json', user)}

        return JsonResponse(result)
    except User.DoesNotExist:
        raise Http404("user does not exist")
