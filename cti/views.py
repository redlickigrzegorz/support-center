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


def login(request):
    next = request.GET.get('next', 'index')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(next)
            else:
                return render(request, 'cti/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'cti/login.html', {'error_message': 'Invalid login'})
    return render(request, "cti/login.html", {'redirect_to': next})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('cti:login'))


@login_required
def index(request):
    template = loader.get_template('cti/index.html')
    faults = Fault.objects.filter(is_visible=True, status__in=[0,1])

    context = {'faults': faults,
               'fields': Fault().get_fields() }

    return HttpResponse(template.render(context, request))


@login_required
def my_faults(request):
    template = loader.get_template('cti/my_faults.html')
    faults = Fault.objects.filter(issuer=request.user.get_username(), is_visible=True)

    context = {'faults': faults,
               'fields': Fault().get_fields(), }

    return HttpResponse(template.render(context, request))


@login_required
def detail(request, fault_id):
    template = loader.get_template('cti/detail.html')
    try:
        fault = Fault.objects.get(pk=fault_id)
        context = {'fault': fault }
    except Fault.DoesNotExist:
        raise Http404("Fault does not exist")

    return HttpResponse(template.render(context, request))


@login_required
def add_fault(request):
    template = loader.get_template('cti/add_fault.html')

    if request.method == "POST":
        form = FaultForm(request.POST)
        if form.is_valid():
            error = form.save(commit=False)
            error.save()
            messages.success(request, "fault added successful")
    else:
        form = FaultForm()

    context = {'form': form,
               'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S") }

    return HttpResponse(template.render(context, request))


@login_required
def edit_fault(request, fault_id):
    template = loader.get_template('cti/edit_fault.html')

    try:
        fault = Fault.objects.get(pk=fault_id)
        form = FaultForm(request.POST or None, instance=fault)

        if request.method == "POST":
            if form.is_valid():
                fault = form.save(commit=False)
                fault.save()
                messages.success(request, "fault edited successful")

        context = {'form': form,
                   'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S") }

        return HttpResponse(template.render(context, request))

    except Fault.DoesNotExist:
        raise Http404("Fault does not exist")


@login_required
def delete_fault(request, fault_id):
    template = loader.get_template('cti/index.html')

    try:
        fault = Fault.objects.get(pk=fault_id)

        if fault.is_visible:
            fault.is_visible = False
            fault.save()
            messages.success(request, "fault deleted successful")

        faults = Fault.objects.filter(is_visible=True, status__in=[0,1])

        context = {'faults': faults,
                   'fields': Fault().get_fields(), }

        return HttpResponse(template.render(context, request))

    except Fault.DoesNotExist:
        raise Http404("Fault does not exist")


@login_required
def assign_to_me(request, fault_id):
    template = loader.get_template('cti/index.html')

    try:
        fault = Fault.objects.get(pk=fault_id)

        if fault.handler == '0' or fault.handler == '':
            fault.handler = request.user.get_username()
            fault.status = 1
            fault.save()
            messages.success(request, "fault assigned successful")
        else:
            messages.warning(request, "fault is already assigned")

        faults = Fault.objects.filter(is_visible=True, status__in=[0,1])

        context = {'faults': faults,
                   'fields': Fault().get_fields(), }

        return HttpResponse(template.render(context, request))

    except Fault.DoesNotExist:
        raise Http404("Fault does not exist")


@login_required
def resolved_faults(request):
    template = loader.get_template('cti/index.html')
    faults = Fault.objects.filter(is_visible=True, status=2)

    context = {'faults': faults,
               'fields': Fault().get_fields()}

    return HttpResponse(template.render(context, request))


@login_required
def change_password(request):
    if request.method == "POST":
        old_pass = request.POST['old_password']
        new_pass = request.POST['new_password']
        new_pass_repeat = request.POST['new_password_repeat']
        user = User.objects.get(username__exact=request.user)
        if new_pass != new_pass_repeat:
            messages.warning(request, 'New password fields are different! ')
        if not user.check_password(old_pass):
            messages.warning(request, 'Old password is wrong')
        if user.check_password(old_pass) and new_pass == new_pass_repeat:
            user.set_password(new_pass)
            user.save()
            user = authenticate(username=request.user, password=new_pass)
            auth.login(request, user)
            messages.success(request, 'Password has been changed')
            return HttpResponseRedirect(reverse('cti:index'))

    return render(request, 'cti/change_password.html')


def login_mobile(request):
    template = loader.get_template('cti/login_mobile.html')
    context = {'login_status': "false"}

    if request.method == "POST":
        username = request.POST['index_no']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                context = {'login_status': "true"}
                return HttpResponse(template.render(context, request))
            else:
                return HttpResponse(template.render(context, request))
        else:
            return HttpResponse(template.render(context, request))

    return HttpResponse(template.render(context, request))


@login_required
def logout_mobile(request):
    template = loader.get_template('cti/login_mobile.html')
    context = {'login_status': "false"}

    auth.logout(request)

    return HttpResponse(template.render(context, request))


@login_required
def index_mobile(request):
    template = loader.get_template('cti/index_mobile.html')
    faults = Fault.objects.filter(is_visible=True, status__in=[0,1])

    serialized_obj = serializers.serialize('json', faults)
    context = {'faults': serialized_obj}

    return HttpResponse(template.render(context, request))


@login_required
def my_faults_mobile(request):
    template = loader.get_template('cti/my_faults_mobile.html')
    faults = Fault.objects.filter(issuer=request.user.get_username(), is_visible=True)

    serialized_obj = serializers.serialize('json', faults)
    context = {'faults': serialized_obj}

    return HttpResponse(template.render(context, request))


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

                context = {'add_fault_status': "true"}

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
