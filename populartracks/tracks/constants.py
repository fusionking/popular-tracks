import os

from django.conf import settings

# General status codes
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_INTERNAL_SERVER_ERROR = 500

# Custom status codes
GENRE_NOT_FOUND = 100
ARTIST_NOT_FOUND = 101

ARTIST_NOT_FOUND_ERROR = 'The requested artist could not be found.'
GENRE_NOT_FOUND_ERROR = 'The requested genre could not be found.'
SET_TOKEN_SUCCESSFUL = 'The access token is set successfully.'
SET_TOKEN_ERROR = 'There was an error in setting the access token.'
SEARCH_ERROR = 'There was an error conducting the artist search.'
TRACKS_ERROR = 'There was an error in finding popular tracks.'
DEFAULT_ERROR = 'There was an error.'

DEFAULT_SUCCESS = 'The request was processed successfully.'
TRACKS_SUCCESS = 'The tracks are successfully found.'

SERVICE_CODES = {
    ARTIST_NOT_FOUND: {
        'artist': ARTIST_NOT_FOUND_ERROR
    },
    HTTP_OK: {
        'accounts': SET_TOKEN_SUCCESSFUL,
        'tracks': TRACKS_SUCCESS
    },
    HTTP_BAD_REQUEST: {
        'accounts': SET_TOKEN_ERROR,
        'search': SEARCH_ERROR,
        'tracks': TRACKS_ERROR
    },
    HTTP_INTERNAL_SERVER_ERROR: {
        'accounts': SET_TOKEN_ERROR,
        'search': SEARCH_ERROR,
        'tracks': TRACKS_ERROR
    },
    GENRE_NOT_FOUND: {
        'genre': GENRE_NOT_FOUND_ERROR
    }
}

SPOTIFY_BASE_URL = 'spotify.com'
SPOTIFY_CONFIG = {
    'accounts': '{}://{}.{}/api/token'.format(
        settings.DEFAULT_SCHEMA, 'accounts', SPOTIFY_BASE_URL
    ),
    'search': '{}://api.{}/v1/search'.format(
        settings.DEFAULT_SCHEMA, SPOTIFY_BASE_URL
    ),
    'tracks': '{}/top-tracks',
}

# TODO get these from dockerfile
CLIENT_ID = os.environ.get('CLIENT_ID', '0238a47b0fdd4c1abb0be769163508f7')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET',
                               '4de1bcb1e61345ca8515f16068d5190e')


GENRES_FILE_PATH = 'data/genres.json'
