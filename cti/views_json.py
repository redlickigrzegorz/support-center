from django.template import loader
from django.http import HttpResponse
from .models import Fault
from django.http import Http404
from .forms import FaultForm
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse


def login(request):
    result = {'login_status': False,
              'error_message': ''}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                result['login_status'] = True
                auth.login(request, user)
            else:
                result['error_message'] = 'your account has been disabled'
        else:
            result['error_message'] = 'invalid login'

    return JsonResponse(result)


@login_required
def logout(request):
    auth.logout(request)

    result = {'login_status': False}

    return JsonResponse(result)


@login_required
def index(request):
    faults = Fault.objects.filter(is_visible=True, status__in=[0,1])

    result = {'faults': serializers.serialize('json', faults)}

    return JsonResponse(result)


@login_required
def my_faults(request):
    faults = Fault.objects.filter(issuer=request.user.get_username(), is_visible=True)

    result = {'faults': serializers.serialize('json', faults)}

    return JsonResponse(result)


@login_required
def resolved_faults(request):
    faults = Fault.objects.filter(is_visible=True, status=2)

    result = {'faults': serializers.serialize('json', faults)}

    return JsonResponse(result)


@login_required
def add_fault(request):
    result = {'add_fault_status': False}

    if request.method == "POST":
        form = FaultForm(request.POST)
        if form.is_valid():
            error = form.save(commit=False)
            error.save()

            result['add_fault_status'] = True

    return JsonResponse(result)


@login_required
def edit_fault(request, fault_id):
    result = {'edit_fault_status': False}

    try:
        fault = Fault.objects.get(pk=fault_id)
        form = FaultForm(request.POST or None, instance=fault)

        if request.method == "POST":
            if form.is_valid():
                fault = form.save(commit=False)
                fault.save()

                result['edit_fault_status'] = True

        return JsonResponse(result)

    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
def delete_fault(request, fault_id):
    result = {'delete_fault_status': False}

    try:
        fault = Fault.objects.get(pk=fault_id)

        if fault.is_visible:
            fault.is_visible = False
            fault.save()

            result['delete_fault_status'] = True

        return JsonResponse(result)

    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
def detail(request, fault_id):
    try:
        fault = Fault.objects.filter(pk=fault_id)
        result = {'fault': serializers.serialize('json', fault)}

        return JsonResponse(result)

    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
def assign_to_me(request, fault_id):
    result = {'assign_fault_status': False}

    try:
        fault = Fault.objects.get(pk=fault_id)

        if fault.handler == '0' or fault.handler == '':
            fault.handler = request.user.get_username()
            fault.status = 1
            fault.save()

            result['assign_fault_status'] = True

        return JsonResponse(result)

    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
def change_password(request):
    result = {'change_password_status': False}

    if request.method == "POST":
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        new_password_repeat = request.POST['new_password_repeat']

        user = User.objects.get(username__exact=request.user)

        if new_password != new_password_repeat:
            messages.warning(request, 'new password fields are different! ')

        if not user.check_password(old_password):
            messages.warning(request, 'old password is wrong')

        if user.check_password(old_password) and new_password == new_password_repeat:
            user.set_password(new_password)
            user.save()
            user = authenticate(username=request.user, password=new_password)
            auth.login(request, user)
            messages.success(request, 'password has been changed')

            result['change_password_status'] = True

    return JsonResponse(result)