from SimpleResolver import SimpleResolver

class Transform(SimpleResolver):
    def __init__(self, field, transform):
        self.field = field
        self.transform = transform
        
    def resolveData(self, data):
        data[self.field] = self.transform(data[self.field])
        return data
