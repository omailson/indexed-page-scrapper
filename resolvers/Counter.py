from CustomField import CustomField

class Counter(CustomField):
    def __init__(self, field):
        self.counter = 0
        super(Counter, self).__init__(field, self.getCounter)

    def getCounter(self, data):
        counter = self.counter
        self.counter = counter + 1
        return counter
