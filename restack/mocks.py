import json
import responses
from restack.connection import BASE_URL, Restack, RESTACK_AUTH_HEADER


def add(url, body, method=responses.GET, status=200):
    responses.add(method, BASE_URL + url, body=body,
                  status=status, content_type='application/json')

def add_callback(url, callback, method=responses.GET):
    responses.add_callback(method, BASE_URL + url, callback, content_type="application/json")

MOCK_TOKEN = "badbeefde5184f5fb9101f899ecbe467"
MOCK_PUBLIC_DEVICES_RESPONSE = '''[{"id":"0aea3bf51a9f4c29b44a4265a8f919d4","name":"Random","description":"Random number generator","visibility":"public","status":"enabled","url":"http://api.restack.io/0aea3bf51a9f4c29b44a4265a8f919d4","created":"2015-02-20T23:34:19Z","updated":"2015-02-20T23:34:19Z"},{"id":"cbfa72b1001f43b880848728484e34e9","name":"Temperature sensor","description":"Measures the temperature in classroom (CampusNorth)","visibility":"public","status":"enabled","url":"http://api.restack.io/cbfa72b1001f43b880848728484e34e9","created":"2015-02-20T20:07:38Z","updated":"2015-02-20T20:07:38Z"},{"id":"ca800b1301e342019fde7178456d3b58","name":"rPI","description":"rPI description","visibility":"public","status":"enabled","url":"http://api.restack.io/ca800b1301e342019fde7178456d3b58","created":"2015-02-20T18:46:50Z","updated":"2015-02-20T19:01:40Z"},{"id":"046544c9987f460da2ae6f08d5c2084e","name":"Humidity Sensor","description":"","visibility":"public","status":"disabled","url":"http://api.restack.io/046544c9987f460da2ae6f08d5c2084e","created":"2015-02-13T19:59:19Z","updated":"2015-02-13T19:59:27Z"},{"id":"3ffea5bac98a42aa842b13eb4cc31a7f","name":"test","description":"","visibility":"public","status":"enabled","url":"http://api.restack.io/3ffea5bac98a42aa842b13eb4cc31a7f","created":"2015-02-12T04:17:46Z","updated":"2015-02-12T04:17:46Z"},{"id":"a735bf8bce5a47859677369824e26ab7","name":"Temp Sensor","description":"","visibility":"public","status":"enabled","url":"http://api.restack.io/a735bf8bce5a47859677369824e26ab7","created":"2015-02-10T21:47:49Z","updated":"2015-02-10T21:47:49Z"}]'''
MOCK_CREATED_DEVICE_RESPONSE = '{"status": "enabled", "updated": "2015-02-10T12:36:37Z", "description": "", "created": "2015-02-10T12:36:37Z", "url": "http://api.restack.io/0aea3bf51a9f4c29b44a4265a8f919d4", "visibility": "private", "key": "d6941aa2c86b478aa0329881317b7f8c", "id": "6e8886ec984045c89024d1e515329fcf", "name": "My device"}'
MOCK_STACKS_RESPONSE = '[{"updated": "2015-02-10T13:31:33Z", "name": "test-stack", "created": "2015-02-10T13:31:04Z", "url": "http://api.restack.io/dac45de08a8b4912b1d7ff76e353a9e4/stack/test-stack", "symbol": "C", "type": "numeric", "unit": "celsius"}]'


def private_devices_callback(request):
    # Do we have a valid token?
    auth_token = request.headers.get(RESTACK_AUTH_HEADER)
    if auth_token != MOCK_TOKEN:
        return 401, {}, json.dumps({'message': 'Invalid token'})
    else:
        return 200, {}, MOCK_PUBLIC_DEVICES_RESPONSE

def add_mock_api():
    add(Restack.ENDPOINT_PUBLIC_DEVICES, body=MOCK_PUBLIC_DEVICES_RESPONSE)
    add_callback(Restack.ENDPOINT_PRIVATE_DEVICES, callback=private_devices_callback)
    add("device", method=responses.POST, body=MOCK_CREATED_DEVICE_RESPONSE, status=201)
    add("device/0aea3bf51a9f4c29b44a4265a8f919d4/stack/Thermometer", method=responses.PUT, body="", status=204)
    add("device/0aea3bf51a9f4c29b44a4265a8f919d4", method=responses.PUT, body="", status=204)
    add("device/0aea3bf51a9f4c29b44a4265a8f919d4/stacks", body=MOCK_STACKS_RESPONSE)
