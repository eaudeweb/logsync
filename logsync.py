import json
import logging
import subprocess
from datetime import datetime
import py


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class LogSyncer(object):

    def __init__(self, **config):
        self.config = config

    def _ssh(self, args, **popen_kwargs):
        host = self.config['host']
        ssh_args = ['ssh', host] + args
        log.info('ssh to %s: %r', host, ssh_args)
        if 'stdout' in popen_kwargs:
            subprocess.check_call(ssh_args, **popen_kwargs)
        else:
            output = subprocess.check_output(ssh_args, **popen_kwargs)
            log.debug('output: %r', output)
            return output

    def sync(self):
        remote_log_file = self.config['remote-path']
        log_files_glob = '%s*' % remote_log_file
        for path in self._ssh(['ls', log_files_glob]).splitlines():
            assert path.startswith(remote_log_file)
            suffix = path[len(remote_log_file):]
            if suffix == '.1':
                break
        else:
            raise ValueError("can't find file to copy")

        # linux: `stat -c %y`
        # macos/bsd: `stat -f %m`
        stat_output = self._ssh(['stat', '-c', '%Y', path])
        log_change_time = datetime.fromtimestamp(int(stat_output))
        now = datetime.now()
        delta = now - log_change_time

        new_file = py.path.local(self.config['local-repo']).join('tmp.log.gz')
        with new_file.open('wb') as f:
            self._ssh(["cat '%s' | gzip" % path], stdout=f)


if __name__ == '__main__':
    import sys
    logging.basicConfig(loglevel=logging.INFO)
    with open(sys.argv[1]) as f:
        LogSyncer(**json.load(f)).sync()
