from SimpleResolver import SimpleResolver

class CustomField(SimpleResolver):
    def __init__(self, field, func):
        self.__field = field
        self.__func = func

    def resolveData(self, data):
        data[self.__field] = self.__func(data)
        return data

