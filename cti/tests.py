from django.test import TestCase
from django.urls import reverse
from .models import Fault, Object, User
import datetime


class FaultModelTest(TestCase):

    def setUp(self):
        self.fault = Fault()

    def test_good_inout_data_for_issuer_field(self):
        self.fault.issuer = '000000'

        self.assertIs(self.fault.validate_issuer_field(), True)

    def test_bad_inout_data_for_issuer_field(self):
        self.fault.issuer = 'issuer'

        self.assertIs(self.fault.validate_issuer_field(), False)

    def test_good_inout_data_for_handler_field(self):
        self.fault.handler = '000000'

        self.assertIs(self.fault.validate_handler_field(), True)

    def test_bad_inout_data_for_handler_field(self):
        self.fault.handler = 'handler'

        self.assertIs(self.fault.validate_handler_field(), False)

    def test_good_inout_data_for_object_number_field(self):
        self.fault.object_number = '0000000000'

        self.assertIs(self.fault.validate_object_number_field(), True)

    def test_bad_inout_data_for_object_number_field(self):
        self.fault.object_number = 'object number'

        self.assertIs(self.fault.validate_object_number_field(), False)

    def test_good_inout_data_for_phone_number_field(self):
        self.fault.phone_number = '000000000'

        self.assertIs(self.fault.validate_phone_number_field(), True)

    def test_bad_inout_data_for_phone_number_field(self):
        self.fault.phone_number = 'phone number'

        self.assertIs(self.fault.validate_phone_number_field(), False)


class ObjectModelTest(TestCase):

    def setUp(self):
        self.fault_object = Object()

    def test_good_inout_data_for_object_number_field(self):
        self.fault_object.object_number = '0000000000'

        self.assertIs(self.fault_object.validate_object_number_field(), True)

    def test_bad_inout_data_for_object_number_field(self):
        self.fault_object.object_number = 'test'

        self.assertIs(self.fault_object.validate_object_number_field(), False)


class ViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='000000', password='password')

        self.fault = Fault(issuer='000000',
                           handler='0',
                           object_number='0000000000',
                           topic='topic',
                           description='description',
                           phone_number='000000000',
                           status=0,
                           priority=1,
                           is_visible=True,
                           watchers='[]')
        self.fault.save()

        self.fault_object = Object(object_number='0000000000',
                                   object_name='object name',
                                   date=datetime.date.today(),
                                   room='room',
                                   status=1,
                                   price=2.00,
                                   comments='comments')
        self.fault_object.save()

        self.client.login(username='000000', password='password')

    def test_call_view_for_login(self):
        response = self.client.get(reverse('cti:login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/client/login.html')

    def test_call_view_for_logout(self):
        response = self.client.get(reverse('cti:logout'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/client/logout.html')

    def test_call_view_for_index(self):
        response = self.client.get(reverse('cti:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/client/index.html')

    def test_call_view_for_my_faults(self):
        response = self.client.get(reverse('cti:my_faults'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/client/index.html')

    def test_call_view_for_watched_faults(self):
        response = self.client.get(reverse('cti:watched_faults'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/client/index.html')

    def test_call_view_for_resolved_faults(self):
        response = self.client.get(reverse('cti:resolved_faults'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/client/index.html')

    def test_call_view_for_sorted_faults(self):
        response = self.client.get(reverse('cti:sorted_faults', args=('topic',)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/client/index.html')

    def test_call_view_for_searched_faults(self):
        response = self.client.get(reverse('cti:searched_faults'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/client/index.html')

    def test_call_view_for_add_fault(self):
        response = self.client.get(reverse('cti:add_fault'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/client/fault_form.html')

    def test_call_view_for_edit_fault(self):
        response = self.client.get(reverse('cti:edit_fault', args=(self.fault.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/client/fault_form.html')

    def test_call_view_for_watch_unwatch_fault(self):
        response = self.client.get(reverse('cti:watch_fault', args=(self.fault.id,)))

        self.assertEqual(response.status_code, 302)

    def test_call_view_for_fault_details(self):
        response = self.client.get(reverse('cti:fault_details', args=(self.fault.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/client/fault_details.html')

    def test_call_view_for_object_details(self):
        response = self.client.get(reverse('cti:object_details', args=(self.fault_object.object_number,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/client/object_details.html')

    def test_call_view_for_user_details(self):
        response = self.client.get(reverse('cti:user_details', args=(self.user.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/client/user_details.html')
