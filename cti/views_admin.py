from django.template import loader
from django.http import HttpResponse
from .models import Fault
from django.http import Http404
from .forms import AdminFaultForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages


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