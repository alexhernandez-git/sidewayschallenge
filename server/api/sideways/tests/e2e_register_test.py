
"""Invitations tests."""

# Django
from django.test import TestCase

# Django REST Framework

# Model

# Utils


class E2ERegisterTests(TestCase):
    """End to end register tests.
        test_register_endpoint_200: should return the request of the two connected devs
        test_register_endpoint_404: should return empty array if not registered
    """

    def setUp(self):

        self.realDev1 = 'MGetwith'
        self.realDev2 = 'MGetwith1'
        self.basePath = '/connected/register'

    def test_register_endpoint_200(self):
        """should return the org when two devs are connected"""
        url = "/connected/realtime/{}/{}/".format(self.realDev1, self.realDev2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        url = "{}/{}/{}/".format(self.basePath, self.realDev1, self.realDev2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)
        self.assertTrue('thisisatestorgname' in response.json()[0]['organizations'])

    def test_register_endpoint_404(self):
        """should return empty array if not registered"""
        url = "{}/random1/random2/".format(self.basePath)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), [])
