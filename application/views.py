from django.shortcuts import render
from .models import Fault


def index(request):
    faults = Fault.objects.all()

    context = {'faults': faults,
               'fields': Fault().get_fields(), }

    return render(request, 'application/index.html', context)