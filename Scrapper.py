from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod
from urlparse import urljoin

from helpers import fetch_page

class Scrapper:
    """This is the main Scrapper class"""

    __metaclass__ = ABCMeta

    def __init__(self, baseUrl):
        """Scrapper constructor

        Args:
            baseUrl (str): The base url to scrap pages from
        """
        self.baseUrl = baseUrl
        self.__resolvers = []

    @abstractmethod
    def getLinks(self, soup):
        """Implement this method to return the list of links of a given page

        Args:
            soup (object): A parse tree object (eg: ``BeautifulSoup``) to read links from

        Returns:
            An iterable containing strings of uris of pages to follow or,
            An iterable containing dictionaries whose `uri` keys contains the page to follow. All keys except `uri` will be added to the final response
        """
        pass

    @abstractmethod
    def getData(self, soup):
        """Implement this method to return the data scrapped from the given page

        Args:
            soup (object): A parse tree object to scrap data from

        Returns:
            A key-value map of the scrapped data
        """
        pass

    def getParsedPage(self, uri=None):
        url = self.buildUrl(uri)
        page = self.fetchPage(url)
        return self.parsePage(page)

    def buildUrl(self, uri):
        """Given a `uri`, return a URL using `self.baseUrl` as base url

        This method can be overwritten if urls shoud be built differently
        """
        return urljoin(self.baseUrl, uri)

    def fetchPage(self, url):
        """Fetchs a page returning its contents

        The return value will be used to build the parse tree object

        This can be rewritten if the page needs to be fetched differently (say from a local source instead of an HTTP server)

        Args:
            url (str): URL to fetch the page from

        Returns:
            A readable unparsed text containing the contents of the page
        """
        return fetch_page(url)

    def parsePage(self, page):
        """Get the parse tree object of a given page

        Can be rewritten if you're using another page parser (default is BeautifulSoup)

        Args:
            page (str): The unparsed page

        Returns:
            A parse tree object of the given page
        """
        return BeautifulSoup(page, 'html.parser')

    def getIndexLinks(self):
        """Get links from the index page"""
        # TODO make private
        page = self.fetchPage(self.baseUrl)
        soup = self.parsePage(page)
        return self.getLinks(soup)

    def getPageData(self, link):
        """Method to get a key-value data from a page given its uri

        `link` can be either a string or a dict containing at least an `uri` key
        If a `dict`, all keys except `uri` will be added to the response
        """
        if isinstance(link, dict):
            uri = link['uri']
        else:
            uri = link
        url = self.buildUrl(uri)
        page = self.fetchPage(url)
        soup = self.parsePage(page)

        data = self.getData(soup)
        data['url'] = data.get('url', url)
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
