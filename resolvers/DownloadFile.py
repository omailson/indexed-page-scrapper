from SimpleResolver import SimpleResolver
import requests

from helpers import save_file

def download_file(url, filename):
    response = requests.get(url)
    save_file(filename, response.content)

class DownloadFile(SimpleResolver):
    def __init__(self, url_field, filename):
        self.urlField = url_field
        self.filename = filename
        
    def resolveData(self, data):
        download_file(data[self.urlField], self.filename(data))
        return data
