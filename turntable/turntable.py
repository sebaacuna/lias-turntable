import logging

logger = logging.getLogger(__name__)

STOPPED = 'Stopped'
PLAYING = 'Playing'
PAUSED = 'Paused'


class Turntable(object):
    """Turntable controller"""

    def __init__(self, mpd):
        self.mpd = mpd
        self.album = None
        self.track = None
        self.track_pos = None
        self.mpd.clear()

    def load(self, album):
        logger.info("Loading {}".format(album))
        self.album = album
        self.mpd.clear()
        self.mpd.load(album.id)

    def unload(self):
        self.mpd.clear()

    def get_status(self):
        return self.mpd.currentsong()

    def play(self):
        self.mpd.play()

    def stop(self):
        self.mpd.stop()

    def next(self):
        self.mpd.next()

    def prev(self):
        self.mpd.previous()
