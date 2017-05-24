from turntable import cli
import click
from json import dumps


@cli.command()
@click.pass_obj
def list_albums(mpd):
    albums = [
        album
        for album in mpd.listplaylists()
    ]
    click.echo(dumps(albums))


@cli.command()
@click.pass_obj
@click.argument('album')
def list_tracks(mpd, album=None):
    if album is None:
        album = 'foo'
    tracks = mpd.listplaylist(album)
    click.echo(dumps(tracks))


@cli.command()
@click.pass_obj
@click.argument('album')
def load_album(mpd, album):
    mpd.clear()
    mpd.load(album)


@cli.command()
@click.pass_obj
def play(mpd):
    mpd.play()


@cli.command()
@click.pass_obj
def stop(mpd):
    mpd.stop()


@cli.command()
@click.pass_obj
def next(mpd):
    mpd.next()


@cli.command()
@click.pass_obj
def prev(mpd):
    mpd.previous()


@cli.command()
@click.pass_obj
@click.argument('volume')
def setvol(mpd, volume):
    mpd.setvol(int(volume))


@cli.command()
@click.pass_obj
def clear(mpd):
    mpd.clear()


@cli.command()
@click.pass_obj
def status(mpd):
    status = mpd.status()
    status.update(mpd.currentsong())
    click.echo(dumps(status))

