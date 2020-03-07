from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from tracks.serializers import TracksSerializer
from tracks.helpers import (
    set_new_access_token, get_genres, get_random_artist,
    get_popular_tracks
)


class GetTokenView(GenericAPIView):
    def get(self, request):
        access_token = set_new_access_token()
        if access_token:
            result = {'message': 'Access token is set successfully.'}
        else:
            result = {'message': (
                'There was an error in settings the access token'
            )}

        return Response(result, status=status.HTTP_200_OK)


class GetTracksView(GenericAPIView):
    serializer_class = TracksSerializer

    def get(self, request, genre):
        genres = get_genres()
        random_artist = get_random_artist(genres, genre)
        if random_artist:
            popular_tracks = get_popular_tracks(random_artist) or []
            # further processing
            serializer = self.get_serializer(data=popular_tracks[:5],
                                             many=True)
            serializer.is_valid(raise_exception=True)
            result = serializer.data
        else:
            result = {'error': 'The provided genre could not be found'}
        # TODO return 400
        return Response(result)
