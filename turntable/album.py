from .track import Track
from pathlib import Path
from itertools import count


class Album:
    def __init__(self, path):
        self.path = Path(path).resolve()
        self.name = path.name
        counter = count()
        self.tracks = [
            Track(
                position=next(counter),
                name=filename.name,
                path=self.path / filename
            )
            for filename in self.path.iterdir()
            if Path(filename).is_file()
        ]

    def __repr__(self):
        return 'Album({.name})'.format(self)
