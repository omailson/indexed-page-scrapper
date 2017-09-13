import json
from SimpleResolver import SimpleResolver

class DumpJson(SimpleResolver):
    def __init__(self, filename, *args, **kwargs):
        if isinstance(filename, basestring):
            self.getFilename = lambda _: filename
        else:
            self.getFilename = filename

        self.args = args
        self.kwargs = kwargs

    def resolveData(self, data):
        with open(self.getFilename(data), 'w') as f:
            json.dump(data, f, *self.args, **self.kwargs) 
        return data
