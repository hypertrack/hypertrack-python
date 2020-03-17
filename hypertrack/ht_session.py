from urllib.parse import urljoin

import requests

from .exceptions import HyperTrackException


class HTSession(requests.Session):
    base_url = None

    def __init__(self, base_url):
        self.base_url = base_url
        super(HTSession, self).__init__()

    def request(self, method, url, *args, **kwargs):
        url = self.create_url(url)
        resp = super(HTSession, self).request(
            method, url, *args, **kwargs
        )

        return self.process_response(resp)

    def create_url(self, url):
        return urljoin(self.base_url, url)

    def build_url(self, *args):
        return '/'.join(args)

    def process_response(self, response):
        if 400 <= response.status_code <= 599:

            try:
                error_resp = response.json()

                if 'status' in error_resp:
                    raise HyperTrackException(**error_resp)
                else:
                    msg = error_resp['message'] if 'message' in error_resp else response.text
                    raise HyperTrackException(status=response.status_code, title=msg, code='generic_error')
            except ValueError:
                raise HyperTrackException(status=response.status_code, title=response.text, code='generic_error')
        else:
            # Might be empty response.
            try:
                resp = response.json()
            except ValueError:
                resp = None

            return resp

