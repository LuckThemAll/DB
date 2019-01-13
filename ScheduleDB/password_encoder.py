import base64


class encoder:
    def __init__(self, raw_password=""):
        self.raw_password = raw_password

    def encode_password(self, raw_password=""):
        if raw_password == "":
            return base64.b64encode(self.raw_password)
        return base64.b64encode(raw_password)
