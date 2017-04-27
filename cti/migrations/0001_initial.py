# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-27 10:50
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Fault',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issuer', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(message='allowed user format: 999999 (6 digits)', regex='^\\d{6}$')])),
                ('handler', models.CharField(default='0', max_length=6, validators=[django.core.validators.RegexValidator(message='allowed user format: 999999 (6 digits) or 0 if nobody is handler', regex='^0|\\d{6}$')])),
                ('object_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='allowed object number format: 9999999999 (10 digits)', regex='^\\d{10}$')])),
                ('topic', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message='allowed phone number format: +999999999 (9-15 digits with possible plus)', regex='^\\+?\\d{9,15}$')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(choices=[(0, 'not started'), (1, 'queued'), (2, 'completed'), (3, 'deleted')], default=0, validators=[django.core.validators.MaxValueValidator(3)])),
                ('priority', models.IntegerField(choices=[(0, 'trivial'), (1, 'standard'), (2, 'urgent')], default=1, validators=[django.core.validators.MaxValueValidator(2)])),
                ('is_visible', models.BooleanField(default=True)),
                ('watchers', models.CharField(default='[]', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('changed_at', models.DateTimeField()),
                ('changed_field', models.CharField(max_length=20)),
                ('previous_version', models.CharField(max_length=200)),
                ('actual_version', models.CharField(max_length=200)),
                ('changer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('fault', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cti.Fault')),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='allowed object number format: 9999999999 (10 digits)', regex='^\\d{10}$')])),
                ('object_name', models.CharField(blank=True, max_length=50)),
                ('date', models.DateField(blank=True)),
                ('room', models.CharField(blank=True, max_length=10)),
                ('status', models.IntegerField(blank=True, choices=[(0, 'missing'), (1, 'located')], validators=[django.core.validators.MaxValueValidator(1)])),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('comments', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]
