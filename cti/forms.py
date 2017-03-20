from django import forms
from .models import Fault


class FaultForm(forms.ModelForm):
    # issuer
    issuer = forms.RegexField(regex=r'^\d{6}$',
                              error_messages={'required': 'this field is required',
                                              'invalid': 'allowed user format: 999999 (6 digits)'})

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
        fields = ['issuer', 'handler', 'object_number', 'topic', 'description', 'phone_number']
