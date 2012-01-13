import json


class LogSyncer(object):

    def __init__(self, **config):
        self.config = config

    def list_remote_files(self):
        print 'list'

    def sync(self):
        self.list_remote_files()


if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as f:
        LogSyncer(**json.load(f)).sync()
