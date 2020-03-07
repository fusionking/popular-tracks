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
    """
    A wrapper for handling network requests.

    Args:
        url: A url string to send the request to.
        data: Either get parameters or the post body dictionary.
        service_name: A string defining the spotify service. (accounts, etc.)
        auth (optional): Basic auth credentials as a tuple.
        headers (optional): Request headers as a dictionary.
        timeout (optional): Seconds to wait before a timeout error is raised.
        method (optional): A method string (get or post)

    Returns:
        result, status_code: A result JSON and a status code as integer.

    Raises:
        SpotifyException: Raised if an error is returned from the external API.
    """
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

    return result, status_code
