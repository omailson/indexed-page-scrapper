import requests
import json
from urlparse import urljoin
from bs4 import BeautifulSoup

def fetch_page(url):
    request = requests.get(url)
    return request.text

def get_soup(url):
    content = fetch_page(url)
    return BeautifulSoup(content, 'html.parser')

def fetch_model_page_mock(uri):
    with open('page.json', 'r') as f:
        data = json.load(f)

    filename = data[uri]
    with open(filename, 'r') as f:
        return f.read()

def fetch_page_mock():
    with open('page.html', 'r') as f:
        data = f.read()
    return data

def save_page(url, filename):
    page = fetch_page(url)
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.prettify('utf-8')
    with open(filename, 'w') as out:
        out.write(content)

def save_index(scrapper):
    save_page(scrapper.baseUrl, 'page.html')

def save_pages(scrapper):
    print 'Fetching index...',
    pages = scrapper.getIndexLinks()
    print 'OK'
    number = 1
    pages_reference = {}
    for page in pages:
        print 'Saving %d...' % (number, ),
        url = urljoin(scrapper.baseUrl, page['uri'])
        filename = 'model%d.html' % number
        save_page(url, filename)
        pages_reference[url] = filename
        number = number + 1
        print 'OK'

    with open('page.json', 'w') as f:
        json.dump(pages_reference, f)
    print 'Done'
