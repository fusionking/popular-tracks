class TracksException(Exception):
    def __init__(self, message, code, *args, **kwargs):
        self.message = message
        self.code = code
        super().__init__(message, code, *args, **kwargs)

    @property
    def as_dict(self):
        return {
            'error': {
                'message': self.message,
                'code': self.code,
            }
        }


class SpotifyException(TracksException):
    pass
