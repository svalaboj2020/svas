from django.test import TestCase

from .models import Entry


class Appointment_ItemTest(TestCase):

    def test_string_representation(self):
        entry = Appointment_Item(patient_name="sreenivas")
        self.assertEqual(str(entry), entry.title)
