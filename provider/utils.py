import urllib.request
from lxml import html

def get_dom(URL):
    response = urllib.request.urlopen(URL)
    r = response.read()
    return html.fromstring(r)
