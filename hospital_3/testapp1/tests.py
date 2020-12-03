from django.test import TestCase
from .models import Registration
# Create your tests here.
class RegistrationTest(TestCase):

    def test_string_representation(self):
        registration = Registration(patient_name="sreenivas")
        self.assertEqual(str(registration), registration.patient_name)
