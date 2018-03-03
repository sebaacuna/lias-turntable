import asyncio
import click
import logging
from turntable import cli

try:
    from RPi import GPIO
except ImportError:
    GPIO = None

try:
    from pirc522 import RFID
except ImportError:
    RFID = None


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@cli.command('daemon')
@click.pass_obj
def main(mpd):
    daemon = Daemon(mpd)
    daemon.run()

class Daemon:
    def __init__(self, mpd):
        self.mpd = mpd

    def run(self):
        self.mpd.clear()
        status = self.mpd.status()
        album = None
        albums = self.mpd.listplaylists()
        volume = Volume(int(status['volume']))
        reader = Reader(wait=0.1)

        while True:
            if volume.changed():
                self.mpd.setvol(volume.value)
                click.echo('{:03d} {}'.format(volume.value, '|' * int(volume.value / 2)))
            tag = reader.read()
            if tag:
                click.echo('Album tag: {}'.format(tag))
                for a in albums:
                    if tag in a['playlist']:
                        album = a
                        break
                if album:
                    self.mpd.clear()
                    self.mpd.load(album['playlist'])
                    self.mpd.play()
                    click.echo(album)

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


class Volume:
    CLK_PIN = 11
    DT_PIN = 12

    def __init__(self, value):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.clk = GPIO.input(self.CLK_PIN)
        self.value = value

    def changed(self):
        clk = GPIO.input(self.CLK_PIN)
        dt = GPIO.input(self.DT_PIN)
        if clk != self.clk:
            change = -1 if dt == clk else 1
            self.value = max(0, min(100, self.value + change))
            self.clk = clk
            return True


class Reader:
    def __init__(self, wait):
        self.read_count = 0
        self.rfid = RFID()
        self.wait = wait
        self.start_reading()

    def start_reading(self):
        self.rfid.init()
        self.rfid.irq.clear()
        self.rfid.dev_write(0x04, 0x00)
        self.rfid.dev_write(0x02, 0xA0)

    def read(self):
        if self.read_count % 100 == 0:
            click.echo('Reader: read: {}'.format(self.read_count))
        self.read_count += 1

        self.rfid.dev_write(0x09, 0x26)
        self.rfid.dev_write(0x01, 0x0C)
        self.rfid.dev_write(0x0D, 0x87)
        if not self.rfid.irq.wait(self.wait):
            return
        self.rfid.irq.clear()
        self.rfid.init()

        tag = self.get_tag()
        self.start_reading()
        click.echo('Reader: tag {}'.format(tag))
        return tag

    def get_tag(self):
        error, tag_type = self.rfid.request()
        if error:
            click.echo('Reader: request error: {} {}'.format(error, tag_type))
            return

        error, uid = self.rfid.anticoll()
        if error:
            click.echo('Reader: anticoll error: {} {}'.format(error, uid))
            return

        return bytearray(uid).hex()
