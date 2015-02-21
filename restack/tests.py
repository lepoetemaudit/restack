import datetime
from unittest import TestCase
import responses
from .connection import Restack, BASE_URL
from restack import RestackError
from restack.entities import Device
from .mocks import MOCK_TOKEN, add_mock_api


class TestErrors(TestCase):

    def setUp(self):
        add_mock_api()


    @responses.activate
    def test_calling_method_requires_token_without_token(self):
        # Create a public-only restack connection
        restack = Restack()
        self.assertRaises(RestackError, restack.get_devices)

        # With a token, it should work fine
        restack = Restack(MOCK_TOKEN)
        restack.get_devices()

    @responses.activate
    def test_calling_with_bad_token(self):
        restack = Restack("Bad token")
        self.assertRaises(RestackError, restack.get_devices)

        # With a token, it should work fine
        restack = Restack(MOCK_TOKEN)
        restack.get_devices()


class TestDeviceListing(TestCase):

    def setUp(self):
        add_mock_api()

    @responses.activate
    def test_public(self):
        responses.add(responses.GET, BASE_URL + Restack.ENDPOINT_PUBLIC_DEVICES, body="['what']")

        restack = Restack()

        device_list = restack.get_public_devices()

        # We should have at least one device
        self.assertTrue(any(device_list))

        # Everything in the list should be an instance of Device
        self.assertTrue(all(isinstance(d, Device) for d in device_list))

        # The devices should have some valid looking data on them, like creation date
        self.assertTrue(isinstance(device_list[0].created, datetime.datetime))

    @responses.activate
    def test_private(self):
        restack = Restack(MOCK_TOKEN)
        device_list = restack.get_devices()

        # Everything in the list should be an instance of Device
        self.assertTrue(all(isinstance(d, Device) for d in device_list))

    @responses.activate
    def test_update(self):
        restack = Restack(MOCK_TOKEN)
        device_list = restack.get_devices()
        device = device_list[0]
        device.name = "New name"
        self.assertTrue(device.save())