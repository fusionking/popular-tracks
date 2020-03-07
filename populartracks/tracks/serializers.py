from rest_framework import serializers, status


class ArtistSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)


class AlbumSerializer(serializers.Serializer):
    images = serializers.JSONField()
    release_date = serializers.CharField(max_length=15)


class TracksSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    artists = ArtistSerializer(many=True)
    album = AlbumSerializer()

    def to_representation(self, track):
        # TODO implement
        artist = track['artists'][0]['name']
        track_name = track['name']
        album_image_url = track['album']['images'][0]['url']
        release_date = track['album']['release_date']
        return {
            'artist': artist,
            'track': track_name,
            'album_image_url': album_image_url,
            'release_date': release_date
        }
