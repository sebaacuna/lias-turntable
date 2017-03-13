import asyncio
import logging
from mpd import MPDClient
from urllib.parse import urlparse
import zmq
import zmq.asyncio


logger = logging.getLogger(__name__)


class Server:
    def __init__(self, listen_url, mpd_url):
        self.url = listen_url
        self.mpd = self._setup_mpd(mpd_url)
        self.mpd.clear()
        self.controls = Controls(self.mpd)

    def _setup_mpd(self, mpd_url):
        urlparts = urlparse(mpd_url)
        mpd = MPDClient()
        mpd.connect(urlparts.hostname, urlparts.port)
        logger.info('Connected to MPD at {}'.format(mpd_url))
        mpd.update()
        return mpd

    def run(self):
        self.ctx = zmq.asyncio.Context()
        self.loop = zmq.asyncio.ZMQEventLoop()
        asyncio.set_event_loop(self.loop)
        self.socket = self.ctx.socket(zmq.REP)
        self.socket.bind(self.url)
        main = self._recv_and_process()
        logger.info('Turntable server started: {.url}'.format(self))

        try:
            self.loop.run_until_complete(main)
        except KeyboardInterrupt:
            pass

        self.controls.clear()
        self.loop.stop()
        self.socket.close()

    @asyncio.coroutine
    def _recv_and_process(self):
        while True:
            try:
                msg = yield from self.socket.recv_json()
                reply = yield from self._handle_command(**msg)
                yield from self.socket.send_json(
                    reply or self.controls.status()
                )
            except Exception as e:
                logger.error(e, exc_info=True)
                yield from self.socket.send_json(str(e))

    @asyncio.coroutine
    def _handle_command(self, command, args=[]):
        logger.info('Received: {}'.format(command))
        return getattr(self.controls, command)(*args)


class Controls:
    def __init__(self, mpd):
        self.mpd = mpd

    def stats(self):
        return self.mpd.status()

    def list_albums(self):
        return [
            album['playlist']
            for album in self.mpd.listplaylists()
        ]

    def list_tracks(self, album_id=None):
        if album_id is None:
            album_id = self.turntable.album.id
        return self.mpd.listplaylist(album_id)

    def load_album(self, album_id):
        self.mpd.clear()
        self.mpd.load(album_id)

    def play(self):
        self.mpd.play()

    def stop(self):
        self.mpd.stop()

    def next(self):
        self.mpd.next()

    def prev(self):
        self.mpd.previous()

    def setvol(self, vol):
        self.mpd.setvol(int(vol))

    def clear(self):
        self.mpd.clear()

    def status(self):
        status = self.mpd.status()
        status.update(self.mpd.currentsong())
        return status
