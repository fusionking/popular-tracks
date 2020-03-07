import requests
import json
import random

from django.core.cache import cache

from tracks.utils import _request
from tracks.constants import (
    CLIENT_ID, CLIENT_SECRET, SPOTIFY_CONFIG,
    HTTP_200_OK, GENRES_FILE_PATH
)


def get_genres():
    with open(GENRES_FILE_PATH) as genres_file:
        genres = json.load(genres_file)
    return genres


def get_random_artist(genres, genre):
    artists = genres.get(genre)
    if not artists:
        return artists
    index = random.randint(0, len(artists) - 1)
    random_artist = artists[index]
    return random_artist


def get_artist_url(response):
    items = response['artists']['items']
    artist_url = items[0]['href'] if items else None
    return artist_url


def set_new_access_token():
    access_token = None
    url = SPOTIFY_CONFIG.get('accounts')
    post_data = {'grant_type': 'client_credentials'}
    response = requests.post(
        url, data=post_data, auth=(CLIENT_ID, CLIENT_SECRET)
    )
    if response.status_code == HTTP_200_OK:
        response = response.json()
        access_token = response['access_token']
        timeout = response['expires_in']
        cache.set('access_token', access_token, timeout=timeout)
    return access_token


def get_artist_search_results(artist, access_token=None):
    access_token = cache.get('access_token')
    if not access_token:
        access_token = set_new_access_token()

    search_url = SPOTIFY_CONFIG.get('search')
    params = {'q': '{}'.format(artist), 'type': 'artist'}
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = _request(
        search_url, data=params, headers=headers
    )
    return response


def get_popular_tracks(artist):
    # Try to get the access token from cache
    access_token = cache.get('access_token')
    if not access_token:
        access_token = set_new_access_token()

    search_results = get_artist_search_results(artist, access_token)

    if search_results:
        artist_url = get_artist_url(search_results)
        if artist_url:
            tracks_url = SPOTIFY_CONFIG.get('tracks').format(artist_url)
            params = {'country': 'TR'}
            headers = {'Authorization': 'Bearer {}'.format(access_token)}
            popular_tracks = _request(tracks_url, params, headers=headers)
            popular_tracks = (
                popular_tracks['tracks'] if popular_tracks else None
            )
        else:
            popular_tracks = None

    return popular_tracks
