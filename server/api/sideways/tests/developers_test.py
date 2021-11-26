
"""Invitations tests."""

# Django
from django.test import TestCase
from collections import namedtuple

# Django REST Framework

# Model
from api.developers.models import Developer, Organization, Register

# Utils
from api.utils import helpers
import requests

# Env
import environ
env = environ.Env()


class DeveloperTests(TestCase):
    """Developer tests.
        test_are_connected: Should return True if the both users are connected
    """

    def setUp(self):

        self.devs_usernames = ['alex', 'MGetwith1']
        self.twitter_token = env("TWITTER_SECRET_KEY")
        self.github_token = env("GITHUB_SECRET_KEY")

    def test_are_connected(self):
        # Retrieve the users from twitter
        is_connected = False
        register = {"connected": False}
        register = namedtuple("ObjectName", register.keys())(*register.values())

        devs = []

        errors = []

        # Get the devs
        for dev_username in self.devs_usernames:
            url = "https://api.twitter.com/2/users/by/username/{}".format(dev_username)
            headers = {"Authorization": "Bearer {}".format(self.twitter_token)}
            result = requests.get(url, headers=headers)
            # If status 200 create the developers
            if result.status_code == 200 and not 'errors' in result.json():
                dev = result.json()['data']
                dev_object = None
                try:
                    dev_object = Developer.objects.get(dev_id=dev['id'])
                    helpers.update_developer(dev_object, dev)
                except Developer.DoesNotExist:
                    dev_object = Developer.objects.create(
                        dev_id=dev['id'],
                        name=dev['name'],
                        username=dev['username'],
                    )
                except Developer.MultipleObjectsReturned:
                    developers = Developer.objects.filter(dev_id=dev['id'])
                    dev_object = developers.first()
                    developers.exclude(dev_object).delete()
                    helpers.update_developer(dev_object, dev)

                devs.append(dev_object)
            else:
                # Error 400
                errors.append("{} is not a valid user in twitter".format(dev_username))

        # There is a list of n length, if all the elements are True means that the developers are following each other
        is_following_developers = [False] * len(self.devs_usernames)
        # Go through the list of developers and see if they follow with the twitter api
        for i, dev in enumerate(devs):
            # Create new set without current user to know if is following the other users
            devs_to_follow = [x for x in devs if x != dev]
            is_following_developers_to_follow = [False] * len(devs_to_follow)

            url = "https://api.twitter.com/2/users/{}/following?max_results=500".format(dev.dev_id)
            result = requests.get(url, headers=headers)
            if 'status' in result.json() and result.json()['status'] == 429:
                errors.append(result.json())
            if result.status_code == 200 and not "errors" in result.json():

                # Save the following devs in dev
                for following_dev in result.json()["data"]:
                    # Get or create the developer
                    dev_to_follow = None
                    try:
                        dev_to_follow = Developer.objects.get(dev_id=following_dev['id'])
                        helpers.update_developer(dev_to_follow, following_dev)

                    except Developer.DoesNotExist:
                        dev_to_follow = Developer.objects.create(
                            dev_id=following_dev['id'],
                            name=following_dev['name'],
                            username=following_dev['username'],
                        )
                    except Developer.MultipleObjectsReturned:
                        developers = Developer.objects.filter(dev_id=following_dev['id'])
                        dev_to_follow = developers.first()
                        developers.exclude(dev_to_follow).delete()
                        helpers.update_developer(dev_to_follow, following_dev)

                    if not dev.following.filter(id=dev_to_follow.id).exists():
                        dev.following.add(dev_to_follow)

                # Check if all the users to follow are in the result
                for y, dev_to_follow in enumerate(devs_to_follow):

                    for dev in result.json()["data"]:

                        if dev_to_follow.dev_id == dev["id"]:
                            is_following_developers_to_follow[y] = True

                if is_following_developers_to_follow and not False in is_following_developers_to_follow:
                    is_following_developers[i] = True

        organizations = []
        # Check if the users have organizatons in commond
        # Put the repeated orgs in dict (org, user)
        for i, dev_username in enumerate(self.devs_usernames):
            url = "https://api.github.com/users/{}/orgs".format(dev_username)
            headers = {"Authorization": "token {}".format(self.github_token)}
            result = requests.get(url, headers=headers)

            if result.status_code == 200:

                for org in result.json():
                    # Get or create the organization
                    try:
                        org_object = Organization.objects.get(org_id=org['id'])
                        helpers.update_organization(org_object, org)

                    except Organization.DoesNotExist:
                        org_object = Organization.objects.create(
                            org_id=org['id'],
                            login=org['login'],
                            node_id=org['node_id'],
                            url=org['url'],
                            repos_url=org['repos_url'],
                            events_url=org['events_url'],
                            hooks_url=org['hooks_url'],
                            issues_url=org['issues_url'],
                            members_url=org['members_url'],
                            public_members_url=org['public_members_url'],
                            avatar_url=org['avatar_url'],
                            description=org['description']
                        )
                    except Organization.MultipleObjectsReturned:
                        orgelopers = Organization.objects.filter(org_id=org['id'])
                        org_object = orgelopers.first()
                        orgelopers.exclude(org_object).delete()
                        helpers.update_organization(org_object, org)

                    organizations += [[]]
                    organizations[i].append(org["login"])

                    dev = None
                    try:
                        dev = Developer.objects.get(username=dev_username)
                    except Developer.MultipleObjectsReturned:
                        developers = Developer.objects.filter(username=dev_username)
                        dev = developers.first()
                        developers.exclude(dev_to_follow).delete()
                    except Developer.DoesNotExist:
                        pass

                    if dev and not dev.organizations.filter(id=org_object.id).exists():

                        dev.organizations.add(org_object)
            else:
                # Raise 400
                errors.append("{} is not a valid user in github".format(dev_username))
                break

        organizations = [x for x in organizations if x != []]
        organizations_objects = None
        if organizations and len(organizations) > 1:
            result = set.intersection(*map(set, organizations))
            # Result: {"org_name", "other_org_name"}
            orgs = [org for org in result]

            if result:
                # Check if are connected
                organizations_objects = Organization.objects.filter(login__in=orgs)
                if organizations_objects.exists() and not False in is_following_developers:
                    is_connected = True
        # Create the register object
        register = Register.objects.create(connected=is_connected)
        if organizations_objects:
            register.organizations.set(organizations_objects)
        if devs:
            register.developers.set(devs)

        print(errors)
        self.assertEqual(register.connected, True)
