from SimpleResolver import SimpleResolver

class CustomField(SimpleResolver):
    def __init__(self, field, getValue):
        self.field = field
        self.getValue = getValue

    def resolveData(self, data):
        data[self.field] = self.getValue(data)
        return data

