from .album import Album
from pathlib import Path


class MusicLibrary:
    def __init__(self, path):
        self.path = Path(path)

    def list_albums(self):
        return [
            Album(path)
            for path in self.path.iterdir()
            if path.is_dir() and not path.name.startswith('.')
        ]

    def get_album(self, album_id):
        return Album(self.path / album_id)
