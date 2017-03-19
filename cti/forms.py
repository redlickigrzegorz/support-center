from django import forms
from .models import Fault
from django.core.validators import MaxValueValidator


class FaultForm(forms.ModelForm):
    # issuer
    issuer = forms.RegexField(regex=r'^\d{6}$', error_message='allowed user format: 999999 (6 digits)')

    # handler
    handler = forms.RegexField(regex=r'^\d{6}$', error_message='allowed user format: 999999 (6 digits)', required=False)

    # object number
    object_number = forms.RegexField(regex=r'^\d{10}$',
                                     error_message='allowed object number format: 9999999999 (10 digits)')

    # topic
    topic = forms.CharField(max_length=50)

    # description
    description = forms.CharField(max_length=200)

    # phone number
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                                    error_message=('allowed phone number format: +999999999 '
                                                   '(9-15 digits with possible plus)'))

    # status
    status_list = (
        (0, 'trivial'),
        (1, 'standard'),
        (2, 'urgent'),
    )
    status = forms.ChoiceField(validators=[MaxValueValidator(2)], choices=status_list, initial=0, required=False)

    # priority
    priority_list = (
        (0, 'not started'),
        (1, 'queued'),
        (2, 'completed'),
    )
    priority = forms.ChoiceField(validators=[MaxValueValidator(2)], choices=priority_list, initial=0, required=False)

    # is visible
    is_visible = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = Fault
        fields = ['issuer', 'phone_number', 'topic', 'description', 'object_number', 'status',
                  'handler', 'priority']