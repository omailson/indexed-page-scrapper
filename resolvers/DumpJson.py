import json
from VoidResolver import VoidResolver

from helpers import dump_json, value_or_callable

class DumpJson(VoidResolver):
    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        self.args = args
        self.kwargs = kwargs

    def call(self, data):
        filename = value_or_callable(self.filename, data)
        dump_json(filename, data, *self.args, **self.kwargs)
