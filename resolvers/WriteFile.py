from VoidResolver import VoidResolver

def save_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

def value_or_callable(val, *args, **kwargs):
    if callable(val):
        return val(*args, **kwargs)
    return val

class WriteFile(VoidResolver):
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content

    def call(self, data):
        filename = value_or_callable(self.filename, data)
        content = value_or_callable(self.content, data)
        save_file(filename, content)
