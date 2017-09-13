from SimpleResolver import SimpleResolver
import requests

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'w') as f:
        f.write(response.content)

class DownloadFile(SimpleResolver):
    def __init__(self, url_field, filename):
        self.urlField = url_field
        self.filename = filename
        
    def resolveData(self, data):
        download_file(data[self.urlField], self.filename(data))
        return data
