from html.parser import HTMLParser
from re import split as resplit
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
from json import load


class htmlParser(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def get_wiki_snippet(res):
    if res['query']['searchinfo']['totalhits'] > 0:
        # get title
        title = res['query']['search'][0]['title']
        # make parser object
        parser = htmlParser()
        # feed snippet to htmlparser
        parser.feed(res['query']['search'][0]['snippet'])
        # get cleaned snippet and split by sentence
        text = resplit(
            r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', parser.get_data())
        return "Results for {}: \n{}".format(title, text[0])
    else:
        return "No results found."


def wiki_search(query):
    try:
        with urlopen("https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&{}".format(urlencode({'srsearch': query}))) as f:
            return get_wiki_snippet(load(f))
    except HTTPError:
        return "No results found."
