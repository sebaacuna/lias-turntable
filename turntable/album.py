# from .track import Track
# from pathlib import Path
# from itertools import count


class Album:
    def __init__(self, library, _id):
        self.id = _id
        self.library = library
        # counter = count()
        # self.tracks = [
        #     Track(
        #         position=next(counter),
        #         name=filename.name,
        #         path=self.path / filename
        #     )
        #     for filename in self.path.iterdir()
        #     if Path(filename).is_file()
        # ]

    def list_tracks(self):
        return self.library.list_tracks(self.id)

    def __repr__(self):
        return self.id
