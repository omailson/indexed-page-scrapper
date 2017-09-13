from BaseResolver import BaseResolver

class Sort(BaseResolver):
    def __init__(self, cmp=None, key=None, reverse=False, blockSize=None):
        self.cmp = cmp
        self.key = key
        self.reverse = reverse
        self.blockSize = blockSize

    def resolve(self, generator):
        dataList = []
        for v in generator:
            dataList.append(v)
            if self.blockSize is not None and len(dataList) >= self.blockSize:
                sortedList = sorted(dataList, self.cmp, self.key, self.reverse)
                for data in sortedList:
                    yield data
                dataList = []

        sortedList = sorted(dataList, self.cmp, self.key, self.reverse)
        for data in sortedList:
            yield data
