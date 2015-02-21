import dateutil.parser
from .exceptions import RestackError


class Device(object):
    PUBLIC = "public"
    PRIVATE = "private"

    def __init__(self, conn=None, response_data=None):
        self.conn = conn
        if response_data:
            fields = "id", "name", "description", "visibility", "status", "url", "created", "updated"
            date_fields = "created", "updated"

            for f in fields:
                val = response_data.get(f)
                if f in date_fields and val is not None:
                    val = dateutil.parser.parse(val)

                setattr(self, f, val)
        else:
            self.id = ""
            self.name = ""
            self.description = ""
            self.visibility = Device.PRIVATE

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