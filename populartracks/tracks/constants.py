import os

HTTP_200_OK = 200

SERVICE_CODES = {}

DEFAULT_SCHEMA = 'https'
SPOTIFY_BASE_URL = 'spotify.com'
SPOTIFY_CONFIG = {
    'accounts': '{}://{}.{}/api/token'.format(
        DEFAULT_SCHEMA, 'accounts', SPOTIFY_BASE_URL
    ),
    'tracks': '{}/top-tracks',
    'search': '{}://api.{}/v1/search'.format(
        DEFAULT_SCHEMA, SPOTIFY_BASE_URL
    )
}

# TODO get these from dockerfile
CLIENT_ID = os.environ.get('CLIENT_ID', '0238a47b0fdd4c1abb0be769163508f7')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET',
                               '4de1bcb1e61345ca8515f16068d5190e')


GENRES_FILE_PATH = 'data/genres.json'
