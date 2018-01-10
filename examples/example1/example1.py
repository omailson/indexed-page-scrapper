# From the project's root folder, execute: python2 -m examples.example1.example1
from Scrapper import Scrapper

URL = 'examples/data1/index.html'

class Example1Scrapper(Scrapper):
    def fetchPage(self, filename):
        # You don't need to overwrite this method if you're fetching a page from a web server
        # We did this because we don't want to start a server just to run this example
        with open(filename, 'r') as f:
            return f.read()

    def getLinks(self, soup):
        li_tags = soup.find_all('li')
        return map(lambda li: li.find('a').get('href'), li_tags)
    
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
    scrapper = Example1Scrapper(URL)
    users = scrapper.execute()
    for u in users:
        print u

if __name__ == '__main__':
    main()
