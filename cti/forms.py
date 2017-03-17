from django import forms
from .models import Fault
from django.core.validators import MaxValueValidator


class FaultForm(forms.ModelForm):
    # issuer
    issuer = forms.RegexField(regex=r'^\d{6}$', error_message='allowed user format: 999999 (6 digits)')

    # handler
    handler = forms.RegexField(regex=r'^\d{6}$', error_message='allowed user format: 999999 (6 digits)')

    # object number
    object_number = forms.RegexField(regex=r'^\d{10}$',
                                     error_message='allowed object number format: 9999999999 (10 digits)')

    # topic
    topic = forms.CharField()

    # description
    description = forms.CharField()

    # phone number
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                                    error_message=('allowed phone number format: +999999999 '
                                                   '(9-15 digits with possible plus)'))

    # date time
    date_time = forms.DateTimeField()

    # status
    status_list = (
        (0, 'trivial'),
        (1, 'standard'),
        (2, 'urgent'),
    )
    status = forms.ChoiceField(validators=[MaxValueValidator(2)], choices=status_list)

    # priority
    priority_list = (
        (0, 'not started'),
        (1, 'queued'),
        (2, 'completed'),
    )
    priority = forms.ChoiceField(validators=[MaxValueValidator(2)], choices=priority_list)

    # is visible
    is_visible = forms.BooleanField()

    class Meta:
        model = Fault
        fields = ['issuer', 'phone_number', 'date_time', 'topic', 'description', 'object_number', 'status',
                  'handler', 'priority']