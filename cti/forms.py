from django import forms
from .models import Fault
from django.core.validators import MaxValueValidator


class FaultForm(forms.ModelForm):
    # object number
    object_number = forms.RegexField(regex=r'^\d{10}$',
                                     error_messages={'required': 'this field is required',
                                                     'invalid': 'allowed object number format: 9999999999 (10 digits)'})

    # topic
    topic = forms.CharField(max_length=50,
                            error_messages={'required': 'this field is required',
                                            'invalid': 'allowed topic max length: 50 signs'})

    # description
    description = forms.CharField(max_length=200,
                                  error_messages={'required': 'this field is required',
                                                  'invalid': 'allowed description max length: 200 signs'})

    # phone number
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                                    error_messages={'required': 'this field is required',
                                                    'invalid': 'allowed phone number format: +999999999 '
                                                               '(9-15 digits with possible plus)'})

    class Meta:
        model = Fault
        fields = ['object_number', 'topic', 'description', 'phone_number']


class AdminFaultForm(forms.ModelForm):
    # issuer
    issuer = forms.RegexField(regex=r'^\d{6}$',
                              error_messages={'required': 'this field is required',
                                              'invalid': 'allowed user format: 999999 (6 digits)'})

    # handler
    handler = forms.RegexField(regex=r'^0|\d{6}$',
                               error_messages={'required': 'this field is required',
                                               'invalid': 'allowed user format: 999999 (6 digits) '
                                                          'or 0 if nobody is handler'})

    # object number
    object_number = forms.RegexField(regex=r'^\d{10}$',
                                     error_messages={'required': 'this field is required',
                                                     'invalid': 'allowed object number format: 9999999999 (10 digits)'})

    # topic
    topic = forms.CharField(max_length=50,
                            error_messages={'required': 'this field is required',
                                            'invalid': 'allowed topic max length: 50 signs'})

    # description
    description = forms.CharField(max_length=200,
                                  error_messages={'required': 'this field is required',
                                                  'invalid': 'allowed description max length: 200 signs'})

    # phone number
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                                    error_messages={'required': 'this field is required',
                                                    'invalid': 'allowed phone number format: +999999999 '
                                                               '(9-15 digits with possible plus)'})

    # status
    status_list = (
        (0, 'trivial'),
        (1, 'standard'),
        (2, 'urgent'),
    )
    status = forms.ChoiceField(validators=[MaxValueValidator(2)], choices=status_list, initial=0)

    # priority
    priority_list = (
        (0, 'not started'),
        (1, 'queued'),
        (2, 'completed'),
    )
    priority = forms.ChoiceField(validators=[MaxValueValidator(2)], choices=priority_list, initial=0)

    # is visible
    is_visible = forms.BooleanField(initial=True)

    class Meta:
        model = Fault
        fields = ['issuer', 'handler', 'object_number', 'topic', 'description',
                  'phone_number', 'status', 'priority', 'is_visible']
