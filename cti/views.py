from django.template import loader
from django.http import HttpResponse
from .models import Fault
from django.http import Http404
from .forms import FaultForm
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.urlresolvers import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


def test(request):
    template = loader.get_template('cti/test.html')

    context = {'fields': Fault().get_fields()}

    return HttpResponse(template.render(context, request))


def login(request):
    template = loader.get_template('cti/login.html')

    context = {'error_message': ''}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)

                return HttpResponseRedirect(reverse('cti:index'))
            else:
                context['error_message'] = 'your account has been disabled'
        else:
            context['error_message'] = 'invalid login'

    return HttpResponse(template.render(context, request))


@login_required
def logout(request):
    auth.logout(request)

    return HttpResponseRedirect(reverse('cti:login'))


@login_required
def index(request):
    template = loader.get_template('cti/index.html')

    faults = Fault.objects.filter(is_visible=True, status__in=[0, 1])

    context = {'faults': faults,
               'fields': Fault().get_fields()}

    return HttpResponse(template.render(context, request))


@login_required
def my_faults(request):
    template = loader.get_template('cti/my_faults.html')

    faults = Fault.objects.filter(issuer=request.user.get_username(), is_visible=True)

    context = {'faults': faults,
               'fields': Fault().get_fields()}

    return HttpResponse(template.render(context, request))


@login_required
def resolved_faults(request):
    template = loader.get_template('cti/index.html')

    faults = Fault.objects.filter(is_visible=True, status=2)

    context = {'faults': faults,
               'fields': Fault().get_fields()}

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
            messages.warning(request, "fault not added {}".format(form.errors))
    else:
        form = FaultForm()

    context = {'form': form,
               'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

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
                   'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        return HttpResponse(template.render(context, request))

    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
def delete_fault(request, fault_id):
    template = loader.get_template('cti/index.html')

    try:
        fault = Fault.objects.get(pk=fault_id)

        if fault.is_visible:
            fault.is_visible = False
            fault.save()
            messages.success(request, "fault deleted successful")

        faults = Fault.objects.filter(is_visible=True, status__in=[0, 1])

        context = {'faults': faults,
                   'fields': Fault().get_fields()}

        return HttpResponse(template.render(context, request))

    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
def detail(request, fault_id):
    template = loader.get_template('cti/detail.html')

    try:
        fault = Fault.objects.get(pk=fault_id)
        context = {'fault': fault}
    except Fault.DoesNotExist:
        raise Http404("fault does not exist")

    return HttpResponse(template.render(context, request))


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

        faults = Fault.objects.filter(is_visible=True, status__in=[0, 1])

        context = {'faults': faults,
                   'fields': Fault().get_fields(), }

        return HttpResponse(template.render(context, request))

    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
def change_password(request):
    template = loader.get_template('cti/change_password.html')

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

            return HttpResponseRedirect(reverse('cti:index'))

    return HttpResponse(template.render(request))
