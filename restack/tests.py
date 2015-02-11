import datetime
from unittest import TestCase
from .connection import Restack, RestackError
from restack.entities import Device

TOKEN = "_a_mock_token_"

class TestErrors(TestCase):
    def test_calling_method_requires_token_without_token(self):
        # Create a public-only restack connection
        restack = Restack()
        self.assertRaises(RestackError, restack.get_devices)

        # With a token, it should work fine
        restack = Restack(TOKEN)
        restack.get_devices()


class TestDeviceListing(TestCase):
    def test_public(self):
        restack = Restack()
        device_list = restack.get_public_devices()

        # We should have at least one device
        self.assertTrue(any(device_list))

        # Everything in the list should be an instance of Device
        self.assertTrue(all(isinstance(d, Device) for d in device_list))

        # The devices should have some valid looking data on them, like creation date
        self.assertTrue(isinstance(device_list[0].created, datetime.datetime))
