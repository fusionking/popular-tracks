import requests

from django.conf import settings

from tracks.constants import (
    DEFAULT_ERROR,
    HTTP_OK,
    SERVICE_CODES
)
from tracks.exc import SpotifyException


def _request(url, data, service_name, auth=None, headers=None,
             timeout=settings.REQUESTS_TIMEOUT, method=settings.METHOD_GET):
    if method == settings.METHOD_GET:
        response = requests.get(
            url, params=data, headers=headers, auth=auth,
            timeout=timeout
        )
    elif method == settings.METHOD_POST:
        response = requests.post(url, data=data, auth=auth)

    status_code = response.status_code

    if status_code != HTTP_OK:
        message = SERVICE_CODES.get(status_code, {}).get(
            service_name, DEFAULT_ERROR
        )
        raise SpotifyException(code=status_code, message=message)

    result = response.json()

    return result, response.status_code
