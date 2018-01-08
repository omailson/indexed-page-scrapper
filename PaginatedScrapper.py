from Scrapper import Scrapper
from abc import ABCMeta, abstractmethod
from urlparse import urljoin

class PaginatedScrapper(Scrapper):
    """This is like ``Scrapper`` but allows you to work on paginated indexes

    Extend this class if the index page (the page containing the links to follow) is paginated
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def getNextPageLink(self, soup):
        """Implement this method to return the link to the next page of a paginated resource

        Since the index page is paginated, we need the link to the next index page

        Should return `None` if on the last page
        """
        pass

    @abstractmethod
    def getPageLinks(self, soup):
        """Implement this method to return the list of links of a given page

        The implementation should be very similar to the one in ``Scrapper.getLinks``. We only had to change the method's name
        """
        pass

    def getLinks(self, soup):
        links = self.getPageLinks(soup)

        for link in links:
            yield link

        nextPageLink = self.getNextPageLink(soup)
        while nextPageLink:
            # TODO soup = self.getParsedPage(nextPageLink)
            url = self.buildUrl(nextPageLink)
            page = self.fetchPage(url)
            soup = self.parsePage(page)

            links = self.getPageLinks(soup)
            for link in links:
                yield link
            nextPageLink = self.getNextPageLink(soup)
