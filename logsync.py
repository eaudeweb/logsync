import json
import logging
import subprocess


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class LogSyncer(object):

    def __init__(self, **config):
        self.config = config

    def _ssh(self, args):
        host = self.config['host']
        log.info('ssh to %s: %r', host, args)
        output = subprocess.check_output(['ssh', host] + args)
        log.debug('output: %r', output)
        return output

    def list_remote_files(self):
        remote_log_file = self.config['remote-path']
        log_files_glob = '%s*' % remote_log_file
        for path in self._ssh(['ls', log_files_glob]).splitlines():
            assert path.startswith(remote_log_file)
            suffix = path[len(remote_log_file):]
            if suffix == '.1':
                print path

    def sync(self):
        self.list_remote_files()


if __name__ == '__main__':
    import sys
    logging.basicConfig(loglevel=logging.INFO)
    with open(sys.argv[1]) as f:
        LogSyncer(**json.load(f)).sync()
