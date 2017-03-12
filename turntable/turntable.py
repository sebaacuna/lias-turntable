import logging
import pygame

logger = logging.getLogger(__name__)

STOPPED = 'Stopped'
PLAYING = 'Playing'
PAUSED = 'Paused'


class Turntable(object):
    """Turntable controller"""

    def __init__(self):
        self.album = None
        self.track = None
        self.track_pos = None
        self.status = STOPPED
        pygame.init()

    def load_album(self, album):
        logger.info("Loading {}".format(album))
        self.album = album
        self.set_track(0)

    def set_track(self, i):
        if i < 0:
            return

        try:
            track = self.album.tracks[i]
            pygame.mixer.music.load(str(track.path))
            pygame.event.poll()
        except IndexError:
            logger.error(
                'Track #{} does not exist on {}'
                .format(i, self.album)
            )
            return
        except Exception:
            logger.error(
                'Error while loading {}'
                .format(track),
                exc_info=True
            )
            return

        self.track = track
        self.track_pos = 0

        logger.info('Set track: {.track}'.format(self))

    def get_status(self):
        return '{0.status}: {0.track} - {0.album}'.format(self)

    def play(self):
        if self.album is None:
            msg = 'No album to play'
            logger.warn(msg)
            return msg
        if self.status == STOPPED:
            logger.info('Starting {}'.format(self.track))
            pygame.mixer.music.play(1, 0.0)
        elif self.status == PAUSED:
            logger.info('Resuming {}'.format(self.track))
            pygame.mixer.music.unpause()
        self.status = PLAYING

    def stop(self):
        pygame.mixer.music.pause()
        self.status = PAUSED

    def next_track(self, skip):
        next_status = self.status
        pygame.mixer.music.stop()
        self.status = STOPPED
        for i in range(10):
            print(i)
            pygame.time.Clock().tick(10)
            if not pygame.mixer.music.get_busy():
                break

        self.set_track(self.track.position + skip)
        if next_status == PLAYING:
            self.play()

        logger.info('Changed track: {.status}'.format(self))
