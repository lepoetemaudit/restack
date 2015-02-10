from unittest import TestCase
from .connection import Restack, RestackError

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
    pass