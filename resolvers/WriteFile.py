from VoidResolver import VoidResolver

from helpers import save_file, value_or_callable

class WriteFile(VoidResolver):
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content

    def call(self, data):
        filename = value_or_callable(self.filename, data)
        content = value_or_callable(self.content, data)
        save_file(filename, content)
