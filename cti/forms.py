from django import forms
from .models import Fault, User


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

    # priority
    priority_list = (
        (0, 'trivial'),
        (1, 'standard'),
        (2, 'urgent'),
    )
    priority = forms.ChoiceField(choices=priority_list, initial=0)

    class Meta:
        model = Fault
        fields = ['object_number', 'topic', 'description', 'priority']


class UserForm(forms.ModelForm):
    # first name
    first_name = forms.RegexField(regex=r'^[A-Z][a-z]+$',
                                  error_messages={'required': 'this field is required',
                                                  'invalid': 'first name must have first capital letter '
                                                             'and rest lowercase'})

    #last name
    last_name = forms.RegexField(regex=r'^[A-Z][a-z]+$',
                                 error_messages={'required': 'this field is required',
                                                 'invalid': 'last name must have first capital letter '
                                                            'and rest lowercase'})

    # email
    email = forms.RegexField(regex=r'^\S+@\S+$',
                             error_messages={'required': 'this field is required',
                                             'invalid': 'email must have \'@\' sign and any white space'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
