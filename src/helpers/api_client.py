import copy
import os
from typing import Dict

import requests
from requests.auth import HTTPBasicAuth
from requests.models import Response


class APIClient(object):
    """
    Default APIClient that uses requests lib to send requests
    """

    def __init__(self, base_url: str, auth=HTTPBasicAuth):
        self.auth = auth
        self.base_url = base_url
        self.default_headers = {}

    def set_auth(self, auth: HTTPBasicAuth):
        self.auth = auth

    def append_default_header(self, key: str, value: str):
        """
        Set default header that will be used in all future requests
        """
        self.default_headers[key] = value

    def get_all_headers(self, headers: Dict[str, str] = None) -> Dict:
        """
        Returns deepcopy dict of default and provided headers
        """
        all_headers = self.default_headers
        if headers:
            headers_copy = copy.deepcopy(self.default_headers)
            headers_copy.update(headers)
            all_headers = headers_copy
        return all_headers

    def get(self, url: str, **kwargs) -> Response:
        headers = self.get_all_headers(headers=kwargs.get("headers"))
        kwargs.update(dict(auth=self.auth, headers=headers))
        return requests.get(self.base_url + url, **kwargs)

    def post(self, url: str, **kwargs) -> Response:
        headers = self.get_all_headers(headers=kwargs.get("headers"))
        kwargs.update(dict(auth=self.auth, headers=headers))
        return requests.post(self.base_url + url, **kwargs)

    def patch(self, url: str, **kwargs) -> Response:
        headers = self.get_all_headers(headers=kwargs.get("headers"))
        kwargs.update(dict(auth=self.auth, headers=headers))
        return requests.patch(self.base_url + url, **kwargs)

    def delete(self, url: str, **kwargs) -> Response:
        headers = self.get_all_headers(headers=kwargs.get("headers"))
        kwargs.update(dict(auth=self.auth, headers=headers))
        return requests.delete(self.base_url + url, **kwargs)
