from BaseResolver import BaseResolver

class Sort(BaseResolver):
    def __init__(self, blockSize=None, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.blockSize = blockSize

    def resolve(self, generator):
        dataList = []
        for v in generator:
            dataList.append(v)
            if self.blockSize is not None and len(dataList) >= self.blockSize:
                sortedList = sorted(dataList, *self.args, **self.kwargs)
                for data in sortedList:
                    yield data
                dataList = []

        sortedList = sorted(dataList, *self.args, **self.kwargs)
        for data in sortedList:
            yield data
