# From the project's root folder, execute: python2 -m examples.example2.example2
from Scrapper import Scrapper
import re

URL = 'examples/data1/index.html'

class Example2Scrapper(Scrapper):
    @staticmethod
    def links_mapper(li_tag):
        a_tag = li_tag.find('a')
        new_user_tag = li_tag.find('strong', string=re.compile('New hire'))
        return {'uri': a_tag.get('href'), 'new_user': new_user_tag is not None}

    def fetchPage(self, filename):
        # You don't need to overwrite this method if you're fetching a page from a web server
        # We did this because we don't want to start a server just to run this example
        with open(filename, 'r') as f:
            return f.read()

    def getLinks(self, soup):
        li_tags = soup.find_all('li')
        return map(Example2Scrapper.links_mapper, li_tags)
    
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
    scrapper = Example2Scrapper(URL)
    users = scrapper.execute()
    for u in users:
        print u

if __name__ == '__main__':
    main()
