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


class JsonViewTest(TestCase):

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

    def test_call_view_for_login_json(self):
        response = self.client.get(reverse('cti:login_json'))

        self.assertEqual(response.status_code, 200)

    def test_call_view_for_logout_json(self):
        response = self.client.get(reverse('cti:logout_json'))

        self.assertEqual(response.status_code, 200)

    def test_call_view_for_index_json(self):
        response = self.client.get(reverse('cti:index_json'))

        self.assertEqual(response.status_code, 200)

    def test_call_view_for_my_faults_json(self):
        response = self.client.get(reverse('cti:my_faults_json'))

        self.assertEqual(response.status_code, 200)

    def test_call_view_for_watched_faults_json(self):
        response = self.client.get(reverse('cti:watched_faults_json'))

        self.assertEqual(response.status_code, 200)

    def test_call_view_for_resolved_faults_json(self):
        response = self.client.get(reverse('cti:resolved_faults_json'))

        self.assertEqual(response.status_code, 200)

    def test_call_view_for_sorted_faults_json(self):
        response = self.client.get(reverse('cti:sorted_faults_json', args=('topic',)))

        self.assertEqual(response.status_code, 200)

    def test_call_view_for_searched_faults_json(self):
        response = self.client.get(reverse('cti:searched_faults_json'))

        self.assertEqual(response.status_code, 200)

    def test_call_view_for_add_fault_json(self):
        response = self.client.get(reverse('cti:add_fault_json'))

        self.assertEqual(response.status_code, 200)

    def test_call_view_for_edit_fault_json(self):
        response = self.client.get(reverse('cti:edit_fault_json', args=(self.fault.id,)))

        self.assertEqual(response.status_code, 200)

    def test_call_view_for_watch_unwatch_fault_json(self):
        response = self.client.get(reverse('cti:watch_fault_json', args=(self.fault.id,)))

        self.assertEqual(response.status_code, 200)

    def test_call_view_for_fault_details_json(self):
        response = self.client.get(reverse('cti:fault_details_json', args=(self.fault.id,)))

        self.assertEqual(response.status_code, 200)

    def test_call_view_for_object_details_json(self):
        response = self.client.get(reverse('cti:object_details_json', args=(self.fault_object.object_number,)))

        self.assertEqual(response.status_code, 200)

    def test_call_view_for_user_details_json(self):
        response = self.client.get(reverse('cti:user_details_json', args=(self.user.id,)))

        self.assertEqual(response.status_code, 200)


class AdminViewTest(TestCase):

    def setUp(self):

        self.superuser = User.objects.create_superuser(username='000000', email='000000@gmail.com', password='password')
        self.user = User.objects.create_user(username='111111', password='password')

        self.fault = Fault(issuer='111111',
                           handler='000000',
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

    def test_call_view_for_index_admin(self):
        response = self.client.get(reverse('cti:index_admin'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/admin/index.html')

    def test_call_view_for_my_faults_admin(self):
        response = self.client.get(reverse('cti:my_faults_admin'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/admin/index.html')

    def test_call_view_for_watched_faults_admin(self):
        response = self.client.get(reverse('cti:watched_faults_admin'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/admin/index.html')

    def test_call_view_for_resolved_faults_admin(self):
        response = self.client.get(reverse('cti:resolved_faults_admin'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/admin/index.html')

    def test_call_view_for_searched_faults_admin(self):
        response = self.client.get(reverse('cti:searched_faults_admin'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/admin/index.html')

    def test_call_view_for_deleted_faults_admin(self):
        response = self.client.get(reverse('cti:deleted_faults_admin'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/admin/index.html')

    def test_call_view_for_all_users_admin(self):
        response = self.client.get(reverse('cti:all_users_admin'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/admin/users.html')

    def test_call_view_for_all_history_admin(self):
        response = self.client.get(reverse('cti:all_history_admin'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/admin/history.html')

    def test_call_view_for_edit_fault_admin(self):
        response = self.client.get(reverse('cti:edit_fault_admin', args=(self.fault.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/admin/fault_form.html')

    def test_call_view_for_watch_unwatch_fault_admin(self):
        response = self.client.get(reverse('cti:watch_fault_admin', args=(self.fault.id,)))

        self.assertEqual(response.status_code, 302)

    def test_call_view_for_finish_fault_admin(self):
        response = self.client.get(reverse('cti:finish_fault_admin', args=(self.fault.id,)))

        self.assertEqual(response.status_code, 302)

    def test_call_view_for_delete_fault_admin(self):
        response = self.client.get(reverse('cti:delete_fault_admin', args=(self.fault.id,)))

        self.assertEqual(response.status_code, 302)

    def test_call_view_for_assign_to_me_admin(self):
        response = self.client.get(reverse('cti:assign_to_me_admin', args=(self.fault.id,)))

        self.assertEqual(response.status_code, 302)

    def test_call_view_for_reassign_fault_admin(self):
        response = self.client.get(reverse('cti:reassign_fault_admin', args=(self.fault.id, self.superuser.username,)))

        self.assertEqual(response.status_code, 302)

    def test_call_view_for_restore_fault_admin(self):
        response = self.client.get(reverse('cti:restore_fault_admin', args=(self.fault.id,)))

        self.assertEqual(response.status_code, 302)

    def test_call_view_for_edit_user_admin(self):
        response = self.client.get(reverse('cti:edit_user_admin', args=(self.superuser.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/admin/user_form.html')

    def test_call_view_for_block_user_admin(self):
        response = self.client.get(reverse('cti:block_user_admin', args=(self.superuser.id,)))

        self.assertEqual(response.status_code, 302)

    def test_call_view_for_restore_user_admin(self):
        response = self.client.get(reverse('cti:restore_user_admin', args=(self.superuser.id,)))

        self.assertEqual(response.status_code, 302)

    def test_call_view_for_change_password_admin(self):
        response = self.client.get(reverse('cti:change_password_admin'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/admin/change_password.html')

    def test_call_view_for_fault_details_admin(self):
        response = self.client.get(reverse('cti:fault_details_admin', args=(self.fault.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/admin/fault_details.html')

    def test_call_view_for_object_details_admin(self):
        response = self.client.get(reverse('cti:object_details_admin', args=(self.fault_object.object_number,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/admin/object_details.html')

    def test_call_view_for_user_details_admin(self):
        response = self.client.get(reverse('cti:user_details_admin', args=(self.superuser.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/admin/user_details.html')

    def test_call_view_for_ask_for_reassign_admin(self):
        response = self.client.get(reverse('cti:ask_for_reassign_admin',
                                           args=(self.fault.id, self.superuser.username,)))

        self.assertEqual(response.status_code, 302)

    def test_call_view_for_report_phone_number_admin(self):
        response = self.client.get(reverse('cti:report_phone_number_admin', args=(self.fault.id,)))

        self.assertEqual(response.status_code, 302)

    def test_call_view_for_statistics_admin(self):
        response = self.client.get(reverse('cti:statistics_admin'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cti/admin/statistics.html')
