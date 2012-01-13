import json
import logging


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class LogSyncer(object):

    def __init__(self, **config):
        self.config = config

    def _ssh(self, args):
        log.info('ssh to %s: %r', self.config['host'], args)

    def list_remote_files(self):
        log_files_glob = '%s*' % self.config['remote-path']
        self._ssh(['ls', log_files_glob])

    def sync(self):
        self.list_remote_files()


if __name__ == '__main__':
    import sys
    logging.basicConfig(loglevel=logging.INFO)
    with open(sys.argv[1]) as f:
        LogSyncer(**json.load(f)).sync()
