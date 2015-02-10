import requests

BASE_URL = "https://api.restack.io/"


class RestackError(BaseException):
    pass

def requires_auth(method):
    def wrap(m):
        if not m.token:
            raise RestackError("Token must be set to call %s" % method.__name__)
    return wrap

class Restack(object):
    def __init__(self, token=None):
        self.token = token

    def make_request(self, method, endpoint, auth=False):
        req = requests.request(method=method, url=BASE_URL+endpoint)
        if auth:
            pass

    @requires_auth
    def get_devices(self):
        pass

    def get_public_device(self):
        """
        Fetch publicly available devices. Does not require authentication.

        :return: a list of public devices
        """
        pass
