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

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('cti:login'))

def index(request):
    template = loader.get_template('cti/index.html')
    faults = Fault.objects.all()

    context = {'faults': faults,
               'fields': Fault().get_fields(), }

    return HttpResponse(template.render(context, request))


def detail(request, fault_id):
    template = loader.get_template('cti/detail.html')
    try:
        fault = Fault.objects.get(pk=fault_id)
        context = {'fault': fault }
    except Fault.DoesNotExist:
        raise Http404("Fault does not exist")

    return HttpResponse(template.render(context, request))


def add_fault(request):
    template = loader.get_template('cti/add_fault.html')

    if request.method == "POST":
        form = FaultForm(request.POST)
        if form.is_valid():
            error = form.save(commit=False)
            error.save()
    else:
        form = FaultForm()

    context = {'form': form}

    return HttpResponse(template.render(context, request))

def edit_fault(request, fault_id):
    template = loader.get_template('cti/edit_fault.html')

    try:
        fault = Fault.objects.get(pk=fault_id)
        form = FaultForm(request.POST or None, instance=fault)

        if request.method == "POST":
            if form.is_valid():
                fault = form.save(commit=False)
                fault.save()

        context = {'form': form}

        return HttpResponse(template.render(context, request))

    except Fault.DoesNotExist:
        raise Http404("Fault does not exist")
