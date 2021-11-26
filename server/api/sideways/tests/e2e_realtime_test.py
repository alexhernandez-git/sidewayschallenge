
"""E2ERealtimeTests tests."""

# Django
from django.test import TestCase

# Django REST Framework

# Model

# Utils


class E2ERealtimeTests(TestCase):
    """End to end realtime tests.
        test_realtime_endpoint_200: should return the org when two devs are connected
        test_realtime_endpoint_400: should return 400 if one handle does not exist
        test_realtime_endpoint_400_return_one: should return 400 if one handle does not exist in github
        test_realtime_endpoint_404_connected_false: should return 404 if they are not connected
    """

    def setUp(self):

        self.realDev1 = 'MGetwith'
        self.realDev2 = 'MGetwith1'
        self.fakeDev2 = 'ñlaskfleoei'
        self.basePath = '/connected/realtime'

    def test_realtime_endpoint_200(self):
        """should return the org when two devs are connected"""
        url = "{}/{}/{}/".format(self.basePath, self.realDev1, self.realDev2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['connected'])
        self.assertTrue('thisisatestorgname' in response.json()['organizations'])

    def test_realtime_endpoint_400(self):
        "should return 400 if one handle does not exist"
        url = "{}/{}/{}/".format(self.basePath, self.realDev1, self.fakeDev2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('errors' in response.json())
        self.assertTrue('{} is not a valid user in github'.format(self.fakeDev2) in response.json()['errors'])
        self.assertTrue('{} is not a valid user in twitter'.format(self.fakeDev2) in response.json()['errors'])

    def test_realtime_endpoint_400_return_one(self):
        "should return 400 if one handle does not exist in github"
        url = "{}/{}/{}/".format(self.basePath, "chosco_", "castarco")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('errors' in response.json())
        self.assertTrue('{} is not a valid user in github'.format("chosco_") in response.json()['errors'])

    def test_realtime_endpoint_404_connected_false(self):
        "should return 404 if they are not connected"
        url = "{}/{}/{}/".format(self.basePath, "flavio", "castarco")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json()['connected'])
