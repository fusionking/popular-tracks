import json
import random

from django.conf import settings
from django.core.cache import cache

from tracks.utils import _request
from tracks.constants import (
    ARTIST_NOT_FOUND,
    CLIENT_ID, CLIENT_SECRET,
    DEFAULT_ERROR,
    GENRES_FILE_PATH, GENRE_NOT_FOUND,
    SERVICE_CODES, SPOTIFY_CONFIG,
)
from tracks.exc import TracksException


def get_genres():
    """
    Gets the genres file from local file system.

    Returns:
        The genres file as a python dictionary.
    """
    with open(GENRES_FILE_PATH) as genres_file:
        genres = json.load(genres_file)
    return genres


def get_random_artist(genres, genre):
    """
    Gets a random artist from a genre's artist list.

    Args:
        genres: A dictionary of genres to artist lists.
        genre: A string of a specific genre.

    Returns:
        A random artist name string.
    Raises:
        TracksException: Raised if the genre is not found.

    """
    artists = genres.get(genre)
    if not artists:
        message = SERVICE_CODES.get(GENRE_NOT_FOUND, {}).get(
            'genre', DEFAULT_ERROR)
        raise TracksException(code=GENRE_NOT_FOUND, message=message)
    index = random.randint(0, len(artists) - 1)
    random_artist = artists[index]
    return random_artist


def get_artist_url(response):
    """
    Gets an artist url from an artist dictionary.

    Args:
        response: A search result response

        Example:
            {
              "artists": {
              "items": [ {
              "genres": [ ],
              "href": "https://api.spotify.com/v1/artists/08td7MxkoHQkXnWAYD",
              "id": "08td7MxkoHQkXnWAYD8d6Q",
              "type": "artist",
              "uri": "spotify:artist:08td7MxkoHQkXnWAYD8d6Q"
              } ],
            }
           }

    Returns:
        artist_url: The href component of the response.

    Raises:
        TracksException: Raised if no artist is found.
    """
    items = response['artists']['items']
    artist_url = items[0]['href'] if items else None
    if not artist_url:
        message = SERVICE_CODES.get(ARTIST_NOT_FOUND, {}).get(
            'artist', DEFAULT_ERROR)
        raise TracksException(code=ARTIST_NOT_FOUND, message=message)
    return artist_url


def set_new_access_token():
    """
    Gets an access token from the Spotify API and sets the cache value.

    Returns:
        access_token, status_code tuple

    Raises:
        SpotifyException: Raised if an error is returned from the external API.
    """
    access_token = cache.get('access_token')
    status_code = None
    if not access_token:
        url = SPOTIFY_CONFIG.get('accounts')
        post_data = {'grant_type': 'client_credentials'}
        response, status_code = _request(
            url, data=post_data, service_name='accounts',
            auth=(CLIENT_ID, CLIENT_SECRET), method=settings.METHOD_POST
        )

        access_token = response['access_token']
        timeout = response['expires_in']
        cache.set('access_token', access_token, timeout=timeout)

    return access_token, status_code


def get_artist_search_results(artist):
    """
    Searches the artist with the given name from the Spotify API.

    Args:
        artist: The artist name

    Returns:
        response, status_code tuple. Response is a dictionary.

    Raises:
        SpotifyException: Raised if an error is returned from the external API.
    """
    access_token = cache.get('access_token')
    if not access_token:
        access_token = set_new_access_token()

    search_url = SPOTIFY_CONFIG.get('search')
    params = {'q': '{}'.format(artist), 'type': 'artist'}
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response, status_code = _request(
        search_url, data=params, headers=headers, service_name='search'
    )
    return response, status_code


def get_popular_tracks(artist):
    """
    Gets an artist's popular tracks from the Spotify API.

    Args:
        artist: The artist name

    Returns:
        response, status_code tuple. Response is a dictionary.

    Raises:
        SpotifyException: Raised if an error is returned from the external API.
    """
    access_token = cache.get('access_token')
    if not access_token:
        access_token = set_new_access_token()

    search_results, status_code = get_artist_search_results(artist)

    artist_url = get_artist_url(search_results)
    tracks_url = SPOTIFY_CONFIG.get('tracks').format(artist_url)
    params = {'country': 'TR'}
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    popular_tracks, status_code = _request(
        tracks_url, params, headers=headers, service_name='tracks')
    popular_tracks_result = popular_tracks['tracks']

    return popular_tracks_result, status_code
