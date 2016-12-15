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

        if fault.handler == '0':
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
