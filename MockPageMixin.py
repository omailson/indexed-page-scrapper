from helpers import fetch_model_page_mock

class MockPageMixin(object):
    def fetchPage(self, url):
        if url != self.baseUrl:
            return fetch_model_page_mock(url)
        return super(MockPageMixin, self).fetchPage(url)
