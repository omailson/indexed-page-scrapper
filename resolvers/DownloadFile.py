from VoidResolver import VoidResolver
import requests

from helpers import save_file, value_or_callable

def download_file(url, filename):
    response = requests.get(url)
    save_file(filename, response.content)

class DownloadFile(VoidResolver):
    def __init__(self, url_field, filename):
        self.urlField = url_field
        self.filename = filename
        
    def call(self, data):
        filename = value_or_callable(self.filename, data)
        download_file(data[self.urlField], filename)
