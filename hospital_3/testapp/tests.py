from django.test import TestCase

# Create your tests here.
class ProjectTests(TestCase):

    def test_homepage(self):
        response = self.client.get('/shome/')
        self.assertEqual(response.status_code, 200)
