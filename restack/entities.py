import dateutil.parser


class Device(object):
    PUBLIC = "public"

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

