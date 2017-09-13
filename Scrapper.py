from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod
from urlparse import urljoin

from helpers import fetch_page

class Scrapper:
    __metaclass__ = ABCMeta

    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.__resolvers = []

    @abstractmethod
    def getLinks(self, soup):
        pass

    @abstractmethod
    def getData(self, soup):
        pass

    def __fetchPage(self, uri):
        url = urljoin(self.baseUrl, uri)
        return self.fetchPage(url)

    def fetchPage(self, url):
        return fetch_page(url)

    def getIndexLinks(self):
        page = self.fetchPage(self.baseUrl)
        soup = BeautifulSoup(page, 'html.parser')
        return self.getLinks(soup)

    def getPageData(self, link):
        if isinstance(link, dict):
            uri = link['uri']
        else:
            uri = link
        page = self.__fetchPage(uri)
        soup = BeautifulSoup(page, 'html.parser')

        data = self.getData(soup)
        data['url'] = data.get('url', urljoin(self.baseUrl, uri))
        if isinstance(link, dict):
            for key in link.iterkeys():
                if key is not 'uri':
                    data[key] = data.get(key, link[key])
        return data

    def addResolver(self, resolver):
        self.__resolvers.append(resolver)
        return self

    def execute(self):
        def pages():
            for link in self.getIndexLinks():
                yield self.getPageData(link)

        gen = pages()
        for resolver in self.__resolvers:
            gen = resolver.resolve(gen)
        return gen
