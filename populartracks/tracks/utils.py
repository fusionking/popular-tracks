import requests

from django.conf import settings

from tracks.constants import HTTP_200_OK

# TODO add a requests wrapper

METHOD_GET = 'get'
METHOD_POST = 'post'


def _request(url, data, auth=None, headers=None,
             timeout=settings.REQUESTS_TIMEOUT, method=METHOD_GET):
    if method == METHOD_GET:
        response = requests.get(
            url, params=data, headers=headers, auth=auth,
            timeout=timeout
        )
    elif method == METHOD_POST:
        response = requests.post(url, data=data, auth=auth)

    if response.status_code == HTTP_200_OK:
        result = response.json()
    else:
        result = None

    return result
