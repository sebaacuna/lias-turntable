from .album import Album
import logging
# from pathlib import Path

logger = logging.getLogger(__name__)


class MusicLibrary:
    def __init__(self, mpd):
        self.mpd = mpd

    def list_albums(self):
        return [
            self.get_album(album['playlist'])
            for album in self.mpd.listplaylists()
        ]

    def list_tracks(self, album_id):
        return self.mpd.listplaylist(album_id)

    def get_album(self, album_id):
        return Album(self, album_id)
