import asyncio
import click
import logging
from RPi import GPIO
from time import sleep
from turntable import cli
# import zmq
# import zmq.asyncio


logger = logging.getLogger(__name__)


@cli.command('daemon')
@click.pass_obj
def main(mpd):
    daemon = Daemon(mpd)
    daemon.run()
    # loop = asyncio.get_event_loop()
    # daemon = Daemon(mpd)

    # try:
    #     self.loop.run_until_complete(daemon.run())
    # except KeyboardInterrupt:
    #     pass

    # loop.stop()


class Daemon:
    def __init__(self, mpd):
        self.mpd = mpd

    def run(self):
        status = self.mpd.status()
        volume_control = VolumeControl(int(status['volume']))
        while True:
            if volume_control.changed():
                self.mpd.setvol(volume_control.value)
                click.echo('volume: {}'.format(volume_control.value))
            sleep(0.01)

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


class VolumeControl:
    CLK_PIN = 17
    DT_PIN = 18

    def __init__(self, value):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.clk = GPIO.input(self.CLK_PIN)
        self.value = value

    def changed(self):
        clk = GPIO.input(self.CLK_PIN)
        dt = GPIO.input(self.DT_PIN)
        if clk != self.clk:
            print((clk, dt))
            change = -1 if dt == clk else 1
            self.value = max(0, min(100, self.value + change))
            self.clk = clk
            return True
