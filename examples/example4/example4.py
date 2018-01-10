# From the project's root folder, execute: python2 -m examples.example4.example4
from PaginatedScrapper import PaginatedScrapper
import re
import resolvers

URL = 'examples/data3/index.html'

# Our index page is now paginated, we need to fetch links not only from the
# index.html page, but also from all the other index pages
#
# The PaginatedScrapper class does most of the work for us. We just need to
# tell them what's the link for the next index page (if any)
#
# Also, we need to rename our `getLinks` implementation to `getPageLinks`
class Example4Scrapper(PaginatedScrapper):
    @staticmethod
    def links_mapper(li_tag):
        a_tag = li_tag.find('a')
        return a_tag.get('href')

    def fetchPage(self, filename):
        # You don't need to overwrite this method if you're fetching a page from a web server
        # We did this because we don't want to start a server just to run this example
        with open(filename, 'r') as f:
            return f.read()

    def getNextPageLink(self, soup):
        # Get link for the next page. Return None if you're already on the last
        # page (otherwise the PaginatedScrapper would never stop)
        next_tag = soup.find(id='next')
        next_link_tag = next_tag.find('a')
        if next_link_tag is not None:
            return next_link_tag.get('href')
        else:
            return None

    def getPageLinks(self, soup):
        # Since PaginatedScrapper already uses `getLinks` internally, we had to rename our `getLinks` implementation to `getPageLinks`
        li_tags = soup.find_all('li')
        return map(Example4Scrapper.links_mapper, li_tags)
    
    def getData(self, soup):
        data = {}

        name_tag = soup.find('h2')
        phone_tag = soup.find(id='phone')
        company_tag = soup.find(id='company')
        years_active_tag = soup.find(id='years-active')

        data['name'] = name_tag.get_text(strip=True)
        data['phone'] = phone_tag.get_text(strip=True)
        data['company'] = company_tag.get_text(strip=True)
        # This field is saved as string, we need to convert to int if we want to perform any numeric operations on it
        data['years_active'] = years_active_tag.get_text(strip=True)

        return data

def main():
    scrapper = Example4Scrapper(URL)
    # We're now using 2 resolvers. The second resolver is operated on the values returned by the first one
    users = (scrapper
        # First, convert `years_active` field to int
        .addResolver(resolvers.Transform('years_active', lambda years_active: int(years_active)))
        # Then filter them out
        .addResolver(resolvers.Filter(lambda data: data['years_active'] >= 15))
        .execute())

    # Print only users active for at least 15 years
    for u in users:
        print u

if __name__ == '__main__':
    main()
