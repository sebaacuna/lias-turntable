import click
import logging
from mpd import MPDClient
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
@click.option('--mpd-url', envvar='MPD_URL', default='http://localhost:6600')
def cli(ctx, mpd_url):
    urlparts = urlparse(mpd_url)
    mpd = MPDClient()
    mpd.connect(urlparts.hostname, urlparts.port)
    logger.info('Connected to MPD at {}'.format(mpd_url))
    mpd.update()
    ctx.obj = mpd

import turntable.commands  # noqa
import turntable.daemon  # noqa
