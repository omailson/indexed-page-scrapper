from helpers import fetch_page_mock

class MockIndexMixin(object):
    def fetchPage(self, url):
        if url == self.baseUrl:
            return fetch_page_mock()
        return super(MockIndexMixin, self).fetchPage(url)
