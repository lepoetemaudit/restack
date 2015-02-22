import re
import dateutil.parser
from .exceptions import RestackError


class Device(object):
    PUBLIC = "public"
    PRIVATE = "private"

    def __init__(self, conn=None, response_data=None):
        self.conn = conn
        if response_data:
            self._load_from_response_data(response_data)

        else:
            self.id = ""
            self.name = ""
            self.description = ""
            self.visibility = Device.PRIVATE

    def _load_from_response_data(self, response_data):
        fields = "id", "name", "description", "visibility", "status", "url", "created", "updated"
        date_fields = "created", "updated"

        for f in fields:
            val = response_data.get(f)
            if f in date_fields and val is not None:
                val = dateutil.parser.parse(val)
            setattr(self, f, val)

    def save(self):
        """
        Save this device. If it is a new device, this returns a new object
        containing the identifier for the object, but leaves the old device
        as it was. If it is an existing device, this returns True on success.

        :return: A Device object or True on success if updating
        """
        if not self.conn:
            raise RestackError("A device must be attached to a connection")

        return self.conn.update_device(self)

    def delete(self):
        if not self.conn:
            raise RestackError("A device must be attached to a connection")

        return self.conn.delete_device(self)


    def __repr__(self):
        return "<Restack:Device id={0} name='{1}'>".format(self.id, self.name)

    def create_stack(self, name, unit, symbol, stack_type):
        if stack_type not in (Stack.NUMERIC, Stack.ALPHANUMERIC):
            raise RestackError(
                "Stack type must be either `Stack.Numeric` or `Stack.ALPHANUMERIC`")

        stack = Stack(device=self)
        stack.name = name
        stack.unit = unit
        stack.symbol = symbol
        stack.type = stack_type
        self.conn.update_stack(stack)
        return stack

    def get_stacks(self):
        return self.conn.get_stacks(self)

class Stack(object):
    NUMERIC = "numeric"
    ALPHANUMERIC = "alphanumeric"

    def _load_from_response_data(self, response_data):
        fields = "type", "unit", "symbol", "url", "created", "updated"
        date_fields = "created", "updated"
        self._name = response_data.get('name')

        for f in fields:
            val = response_data.get(f)
            if f in date_fields and val is not None:
                val = dateutil.parser.parse(val)
            setattr(self, f, val)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        match = re.match(r"[a-zA-Z0-9-_]*$", value)
        if not match:
            raise RestackError("Stack names must only contain numbers, letters, dashes or underscores")

        self._name = value

    def save(self):
        self.device.conn.update_stack(self)

    def put_data(self, value, timestamp=None):
        return self.device.conn.save_stack_data(self, value, timestamp)

    def __init__(self, device, response_data=None):
        self.device = device

        if not response_data:
            self._name = ""
            self.unit = ""
            self.symbol = ""
            self.type = Stack.NUMERIC
        else:
            self._load_from_response_data(response_data)