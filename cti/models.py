from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MaxValueValidator


class Fault(models.Model):
    user_regex = RegexValidator(regex=r'^\d{6}$', message='allowed user format: 999999 (6 digits)')

    # issuer
    issuer = models.CharField(max_length=6, validators=[user_regex])

    # handler
    handler = models.CharField(max_length=6, validators=[user_regex], blank=True)

    # object number
    object_number_regex = RegexValidator(regex=r'^\d{10}$',
                                         message='allowed object number format: 9999999999 (10 digits)')
    object_number = models.CharField(max_length=10, validators=[object_number_regex])

    # topic
    topic = models.CharField(max_length=50)

    # description
    description = models.CharField(max_length=200)

    # phone number
    phone_number_regex = RegexValidator(regex=r'^\+?\d{9,15}$',
                                        message='allowed phone number format: +999999999 '
                                                '(9-15 digits with possible plus)')
    phone_number = models.CharField(max_length=16, validators=[phone_number_regex], blank=True)

    # date time
    date_time = models.DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # status
    status_list = (
        (0, 'trivial'),
        (1, 'standard'),
        (2, 'urgent'),
    )
    status = models.IntegerField(validators=[MaxValueValidator(2)], choices=status_list, default=0)

    # priority
    priority_list = (
        (0, 'not started'),
        (1, 'queued'),
        (2, 'completed'),
    )
    priority = models.IntegerField(validators=[MaxValueValidator(2)], choices=priority_list, default=0)

    # is visible
    is_visible = models.BooleanField(default=True)

    def get_fields(self):
        all_fields = []

        for field in Fault._meta.fields:
            all_fields.append(field)

        return [(field.name, field.value_to_string(self)) for field in all_fields]

    def __str__(self):
        return self.topic


class User(AbstractUser):
    pass