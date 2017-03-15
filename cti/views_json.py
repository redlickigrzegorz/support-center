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


def test(request):
    faults = Fault.objects.filter(is_visible=True, status__in=[0,1])

    serialized_obj = serializers.serialize('json', faults)
    context = {'faults': serialized_obj}

    return JsonResponse(context)


@login_required
def detail_mobile(request, fault_id):
    template = loader.get_template('cti/detail_mobile.html')
    try:
        fault = Fault.objects.get(pk=fault_id)
        context = {'fault': fault.get_fields() }
    except Fault.DoesNotExist:
        raise Http404("Fault does not exist")

    return HttpResponse(template.render(context, request))


@login_required
def add_fault_mobile(request):
    template = loader.get_template('cti/add_fault_mobile.html')
    context = {'add_fault_status': "false"}

    if request.method == "POST":
        form = FaultForm(request.POST)
        if form.is_valid():
            error = form.save(commit=False)
            error.save()

            context = {'add_fault_status': "true"}

            return HttpResponse(template.render(context, request))

    return HttpResponse(template.render(context, request))


@login_required
def edit_fault_mobile(request, fault_id):
    template = loader.get_template('cti/edit_fault_mobile.html')
    context = {'edit_fault_status': "false"}

    try:
        fault = Fault.objects.get(pk=fault_id)
        form = FaultForm(request.POST or None, instance=fault)

        if request.method == "POST":
            if form.is_valid():
                fault = form.save(commit=False)
                fault.save()

                context = {'edit_fault_status': "true"}

                return HttpResponse(template.render(context, request))

        return HttpResponse(template.render(context, request))

    except Fault.DoesNotExist:
        raise Http404("Fault does not exist")


@login_required
def delete_fault_mobile(request, fault_id):
    template = loader.get_template('cti/delete_fault_mobile.html')
    context = {'delete_fault_status': "false"}

    try:
        fault = Fault.objects.get(pk=fault_id)

        if fault.is_visible:
            fault.is_visible = False
            fault.save()

            context = {'delete_fault_status': "true"}

            return HttpResponse(template.render(context, request))

        return HttpResponse(template.render(context, request))

    except Fault.DoesNotExist:
        raise Http404("Fault does not exist")


@login_required
def assign_to_me_mobile(request, fault_id):
    template = loader.get_template('cti/assign_fault_mobile.html')
    context = {'assign_fault_status': "false"}

    try:
        fault = Fault.objects.get(pk=fault_id)

        if fault.handler == '0' or fault.handler == '':
            fault.handler = request.user.get_username()
            fault.status = 1
            fault.save()

            context = {'assign_fault_status': "true"}

            return HttpResponse(template.render(context, request))

        return HttpResponse(template.render(context, request))

    except Fault.DoesNotExist:
        raise Http404("Fault does not exist")


@login_required
def resolved_faults_mobile(request):
    template = loader.get_template('cti/resolved_faults_mobile.html')
    faults = Fault.objects.filter(is_visible=True, status=2)

    serialized_obj = serializers.serialize('json', faults)
    context = {'faults': serialized_obj}

    return HttpResponse(template.render(context, request))
