import asyncio
import logging
import zmq
import zmq.asyncio

logger = logging.getLogger(__name__)


class Server:
    def __init__(self, turntable, library, url):
        self.url = url
        self.turntable = turntable
        self.library = library
        self.commands = Commands(self)

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

    def list_albums(self):
        return [
            (album.id, album.name)
            for album in self.library.list_albums()
        ]

    def list_tracks(self, album_id=None):
        if album_id is None:
            tracks = self.turntable.album.tracks
        else:
            tracks = self.library.get_album(album_id).tracks
        return '\n'.join(map(str, tracks))

    def load_album(self, album_id):
        album = self.library.get_album(album_id)
        self.turntable.load_album(album)
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
        self.turntable.next_track(+1)
        return self.turntable.get_status()

    def prev(self):
        self.turntable.next_track(-1)
        return self.turntable.get_status()
