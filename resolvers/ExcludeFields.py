from SimpleResolver import SimpleResolver

class ExcludeFields(SimpleResolver):
    def __init__(self, fields):
        self.__fields = fields

    def resolveData(self, data):
        return { k:v for k,v in data.items() if k not in self.__fields }
