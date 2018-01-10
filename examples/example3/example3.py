# From the project's root folder, execute: python2 -m examples.example3.example3
from Scrapper import Scrapper
import re
import resolvers

URL = 'examples/data2/index.html'

class Example3Scrapper(Scrapper):
    @staticmethod
    def links_mapper(li_tag):
        a_tag = li_tag.find('a')
        new_hire_tag = li_tag.find('strong', string=re.compile('New hire'))
        return {'uri': a_tag.get('href'), 'new_hire': new_hire_tag is not None}

    def fetchPage(self, filename):
        # You don't need to overwrite this method if you're fetching a page from a web server
        # We did this because we don't want to start a server just to run this example
        print 'Fetching... %s' % filename
        with open(filename, 'r') as f:
            return f.read()

    def getLinks(self, soup):
        li_tags = soup.find_all('li')
        return map(Example3Scrapper.links_mapper, li_tags)
    
    def getData(self, soup):
        data = {}

        name_tag = soup.find('h2')
        phone_tag = soup.find(id='phone')
        company_tag = soup.find(id='company')

        data['name'] = name_tag.get_text(strip=True)
        data['phone'] = phone_tag.get_text(strip=True)
        data['company'] = company_tag.get_text(strip=True)

        return data

def main():
    scrapper = Example3Scrapper(URL)
    # Using a resolver to limit the number of results
    # The evaluation on most of the resolvers is lazy, thus only the first 10 pages are actually fetched
    users = (scrapper
        .addResolver(resolvers.Limit(10))
        .execute())
    for u in users:
        print u

if __name__ == '__main__':
    main()
