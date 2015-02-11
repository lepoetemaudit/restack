import requests
from restack.entities import Device

BASE_URL = "https://api.restack.io/"


class RestackError(BaseException):
    pass


def requires_auth(method):
    def wrap(m):
        if not m.token:
            raise RestackError("Token must be set to call %s" % method.__name__)
    return wrap


class Restack(object):
    """
    The basic Restack connection object
    """

    def __init__(self, token=None):
        self.token = token

    def make_request(self, endpoint, method="GET", auth=False):
        headers = {}
        if auth:
            headers['X-RSTCK-KEY'] = self.token

        return requests.request(method=method, url=BASE_URL+endpoint, headers={})

    @requires_auth
    def get_devices(self):
        pass

    def get_public_devices(self):
        """
        Fetch publicly available devices. Does not require authentication.

        :return: a list of public devices
        """
        resp = self.make_request("devices/list")
        return [Device(conn=self, response_data=d) for d in resp.json()]