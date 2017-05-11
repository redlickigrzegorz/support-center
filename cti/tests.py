from django.test import TestCase
from .models import Fault, Object


class FaultModelTest(TestCase):

    def setUp(self):
        self.fault = Fault()

    def test_good_inout_data_for_issuer_field(self):
        self.fault.issuer = '000000'

        self.assertIs(self.fault.validate_issuer_field(), True)

    def test_bad_inout_data_for_issuer_field(self):
        self.fault.issuer = 'test'

        self.assertIs(self.fault.validate_issuer_field(), False)

    def test_good_inout_data_for_handler_field(self):
        self.fault.handler = '000000'

        self.assertIs(self.fault.validate_handler_field(), True)

    def test_bad_inout_data_for_handler_field(self):
        self.fault.handler = 'test'

        self.assertIs(self.fault.validate_handler_field(), False)

    def test_good_inout_data_for_object_number_field(self):
        self.fault.object_number = '0000000000'

        self.assertIs(self.fault.validate_object_number_field(), True)

    def test_bad_inout_data_for_object_number_field(self):
        self.fault.object_number = 'test'

        self.assertIs(self.fault.validate_object_number_field(), False)

    def test_good_inout_data_for_phone_number_field(self):
        self.fault.phone_number = '000000000'

        self.assertIs(self.fault.validate_phone_number_field(), True)

    def test_bad_inout_data_for_phone_number_field(self):
        self.fault.phone_number = 'test'

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
