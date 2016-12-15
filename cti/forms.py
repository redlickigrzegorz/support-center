from django import forms
from .models import Fault


class FaultForm(forms.ModelForm):
    issuer = forms.IntegerField()
    phone_number = forms.IntegerField()
    date_time = forms.CharField()
    topic = forms.CharField()
    description = forms.CharField()
    object_number = forms.IntegerField()
    status = forms.IntegerField()
    handler = forms.CharField()
    priority = forms.IntegerField()
    is_visible = forms.BooleanField()

    class Meta:
        model = Fault
        fields = ['issuer', 'phone_number', 'date_time', 'topic', 'description', 'object_number', 'status',
                  'handler', 'priority']