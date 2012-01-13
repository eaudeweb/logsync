import json
import logging


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class LogSyncer(object):

    def __init__(self, **config):
        self.config = config

    def _ssh(self, args):
        log.debug('ssh to %s: %r', self.config['host'], args)

    def list_remote_files(self):
        self._ssh(['ls', self.config['remote-path']])

    def sync(self):
        self.list_remote_files()


if __name__ == '__main__':
    import sys
    logging.basicConfig(loglevel=logging.DEBUG)
    with open(sys.argv[1]) as f:
        LogSyncer(**json.load(f)).sync()
