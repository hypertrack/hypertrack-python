from base64 import b64encode

from .devices import Devices
from .ht_session import HTSession
from .trips import Trips

BASE_URL = "https://v3.api.hypertrack.com/"


class Client:

    def __init__(self, account_id, secret_key):
        self.account_id = account_id
        self.secret_key = secret_key

        self.requests = HTSession(base_url=BASE_URL)
        self.requests.headers.update({
            'Authorization': 'Basic {}'.format(self._encode_credentials(account_id, secret_key))
        })

    def _encode_credentials(self, account_id, secret_key):
        return b64encode('{}:{}'.format(account_id, secret_key).encode('ascii')).decode('utf-8')

    @property
    def devices(self):
        return Devices(requests=self.requests)

    @property
    def trips(self):
        return Trips(requests=self.requests)
