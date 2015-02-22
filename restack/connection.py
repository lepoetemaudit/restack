import datetime
import json
import requests
from restack.entities import Device, Stack
from restack.exceptions import RestackError

BASE_URL = "https://api.restack.io/"
RESTACK_AUTH_HEADER = "X-RSTCK-KEY"


def requires_auth(method):
    def wrap(m, *args, **kwargs):
        if not m.token:
            raise RestackError("Token must be set to call %s" % method.__name__)
        else:
            return method(m, *args, **kwargs)
    return wrap


class Restack(object):
    """
    The basic Restack connection object
    """

    ENDPOINT_PRIVATE_DEVICES = "devices"
    ENDPOINT_PUBLIC_DEVICES = "devices/list"

    def __init__(self, token=None):
        self.token = token

    def _build_device_list(self, resp):
        return [Device(conn=self, response_data=d) for d in resp.json()]

    def _build_stack_list(self, device, resp):
        return [Stack(device=device, response_data=d) for d in resp.json()]

    def make_request(self, endpoint, method="GET", auth=False, body=None):
        headers = {}
        if auth:
            headers[RESTACK_AUTH_HEADER] = self.token

        resp = requests.request(method=method, url=BASE_URL+endpoint, headers=headers, data=body)
        if resp.status_code == 401:
            raise RestackError("Unauthorized to make this call. Message: '%s'" % resp.json().get('message', "unknown"))

        return resp

    @requires_auth
    def update_device(self, device):

        if device.id:
            method = "PUT"
            endpoint = "device/%s" % device.id
        else:
            method = "POST"
            endpoint = "device"

        body = {
            'name': device.name,
            'description': device.description,
            'visibility': device.visibility
        }

        resp = self.make_request(endpoint=endpoint,
                                 method=method, auth=True, body=json.dumps(body))

        # If updating, check whether the update was successful
        if device.id:
            return resp.status_code == 204

        if resp.status_code != 201:
            data = resp.json()
            raise RestackError("Couldn't save device. Message: %s; Errors: %s"
                               % (data.get('message'), data.get('errors', None)))


        device._load_from_response_data(resp.json())

    def get_device(self, device_id):
        resp = self.make_request(endpoint="device/%s" % device_id, auth=True)
        if resp.status_code == 200:
            return Device(conn=self, response_data=resp.json())
        elif resp.status_code == 401:
            raise RestackError("You are not authorized to see this device")

    @requires_auth
    def delete_device(self, device):
        if not device.id:
            raise RestackError("Cannot delete a device that hasn't been saved or doesn't have an id")

        resp = self.make_request(endpoint="device/%s" % device.id, auth=True, method="DELETE")
        return resp.status_code == 204

    @requires_auth
    def get_devices(self):
        """
        Fetch devices associated with this account. Requires authentication.

        :return: a list of devices
        """

        return self._build_device_list(
            self.make_request(self.ENDPOINT_PRIVATE_DEVICES, auth=True))

    def get_public_devices(self):
        """
        Fetch publicly available devices. Does not require authentication.

        :return: a list of public devices
        """

        return self._build_device_list(
            self.make_request(self.ENDPOINT_PUBLIC_DEVICES))

    @requires_auth
    def update_stack(self, stack):
        endpoint = "device/%s/stack/%s" % (stack.device.id, stack.name)
        method = "PUT"

        body = dict((k, getattr(stack, k, None)) for k in ('unit', 'symbol', 'type'))

        resp = self.make_request(endpoint=endpoint,
                                 method=method, auth=True, body=json.dumps(body))

        return resp.status_code == 204

    @requires_auth
    def get_stacks(self, device):
        endpoint = "device/%s/stacks" % device.id
        return self._build_stack_list(device, self.make_request(endpoint, auth=True))

    @requires_auth
    def save_stack_data(self, stack, value, timestamp=None):
        body = {'value': str(value)}

        if not timestamp:
            timestamp = datetime.datetime.utcnow() - datetime.timedelta(hours=10)
        body['timestamp'] = timestamp.isoformat() + "Z"

        endpoint = "device/%s/stack/%s/value" % (stack.device.id, stack.name)

        resp = self.make_request(endpoint=endpoint,
                             method="POST", auth=True, body=json.dumps(body))

        return resp.status_code in (201, 202)