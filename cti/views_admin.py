from django.template import loader
from django.http import HttpResponse
from .models import Fault, Object
from django.http import Http404
from .forms import FaultForm, AdminFaultForm
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from .backends import InvbookBackend
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.db.models import Q
from .views import post_faults_to_session, get_faults_from_session


@login_required
@staff_member_required
def index(request):
    template = loader.get_template('cti/admin_index.html')

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
               'header': 'all faults'}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def edit_fault(request, fault_id):
    template = loader.get_template('cti/admin_edit_fault.html')

    try:
        fault = Fault.objects.get(pk=fault_id)
        form = AdminFaultForm(request.POST or None, instance=fault)

        if request.method == "POST":
            if form.is_valid():
                fault = form.save(commit=False)
                fault.save()
                messages.success(request, "fault edited successful")

        context = {'form': form}

        return HttpResponse(template.render(context, request))

    except Fault.DoesNotExist:
        raise Http404("fault does not exist")