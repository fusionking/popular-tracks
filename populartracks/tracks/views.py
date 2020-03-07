from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from tracks.constants import (DEFAULT_SUCCESS, SERVICE_CODES)
from tracks.serializers import TracksSerializer
from tracks.helpers import (
    set_new_access_token, get_genres, get_random_artist,
    get_popular_tracks
)
from tracks.exc import TracksException, SpotifyException


class SetTokenView(GenericAPIView):
    def post(self, request):
        try:
            access_token, status_code = set_new_access_token()
            # We are sure that the access token is set
            message = SERVICE_CODES.get(status_code, {}).get(
                'accounts', DEFAULT_SUCCESS
            )
            result = {
                'code': status_code,
                'message': message
            }
        except SpotifyException as e:
            result = e.as_dict

        response = Response(result, status=status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "*"
        return response


class GetTracksView(GenericAPIView):
    serializer_class = TracksSerializer

    def get(self, request, genre):
        genres = get_genres()
        result = {}

        try:
            random_artist = get_random_artist(genres, genre)
            popular_tracks, status_code = get_popular_tracks(random_artist)
            # further processing
            serializer = self.get_serializer(data=popular_tracks[:5],
                                             many=True)
            serializer.is_valid(raise_exception=True)
            message = SERVICE_CODES.get(status_code, {}).get(
                'tracks', DEFAULT_SUCCESS
            )
            result = {
                'code': status_code,
                'message': message,
                'result': serializer.data
            }
        except (TracksException, SpotifyException) as e:
            result = e.as_dict

        response = Response(result, status=status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "*"
        return response
