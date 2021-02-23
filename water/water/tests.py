from django.test import TestCase


class MainTest(TestCase):
    def test_root_view(self):
        response = self.client.get("")
        self.assertEqual(200, response.status_code)
