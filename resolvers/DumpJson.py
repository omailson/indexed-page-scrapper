import json
from SimpleResolver import SimpleResolver

from helpers import dump_json

class DumpJson(SimpleResolver):
    def __init__(self, filename, *args, **kwargs):
        if isinstance(filename, basestring):
            self.getFilename = lambda _: filename
        else:
            self.getFilename = filename

        self.args = args
        self.kwargs = kwargs

    def resolveData(self, data):
        dump_json(self.getFilename(data), data, *self.args, **self.kwargs)
        return data
