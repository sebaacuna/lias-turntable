from .turntable import Turntable
from .musiclibrary import MusicLibrary
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
        mpd = self._setup_mpd(mpd_url)
        self.turntable = Turntable(mpd)
        self.library = MusicLibrary(mpd)
        self.commands = Commands(self)

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

        self.turntable.unload()
        self.loop.stop()
        self.socket.close()

    @asyncio.coroutine
    def _recv_and_process(self):
        while True:
            try:
                msg = yield from self.socket.recv_json()
                reply = yield from self._handle_command(**msg)
                yield from self.socket.send_json(reply)
            except Exception as e:
                logger.error(e, exc_info=True)
                yield from self.socket.send_json(str(e))

    @asyncio.coroutine
    def _handle_command(self, command, args=[]):
        logger.info('Received: {}'.format(command))
        return getattr(self.commands, command)(*args)


class Commands:
    def __init__(self, server):
        self.turntable = server.turntable
        self.library = server.library

    def stats(self):
        return self.mpd.status()

    def list_albums(self):
        return list(map(str, self.library.list_albums()))

    def list_tracks(self, album_id=None):
        album = self.library.get_album(
            album_id or self.turntable.album.id
        )
        return album.list_tracks()

    def load_album(self, album_id):
        album = self.library.get_album(album_id)
        self.turntable.load(album)
        return self.turntable.get_status()

    def status(self):
        return self.turntable.get_status()

    def play(self):
        self.turntable.play()
        return self.turntable.get_status()

    def stop(self):
        self.turntable.stop()
        return self.turntable.get_status()

    def next(self):
        self.turntable.next()
        return self.turntable.get_status()

    def prev(self):
        self.turntable.prev()
        return self.turntable.get_status()
