from django.test import TestCase
from django.test import TransactionTestCase


class MainTest(TransactionTestCase):
    def test_root_view(self):
        response = self.client.get("")
        self.assertEqual(200, response.status_code)
