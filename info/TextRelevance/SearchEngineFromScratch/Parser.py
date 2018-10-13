from bs4 import BeautifulSoup

from utils import clear_text



class Parser():
    def __init__(self):
        pass


    def get_marks(self, text):
        soup = BeautifulSoup(text, "lxml")

        for s in soup.findAll(['script', 'style']):
            s.decompose()

        def get_a(soup):
            try:
                links = '\n'.join(link.extract().get_text().lower() for link in soup('a'))
                links = clear_text(links)
            except:
                links = []
            return links

        def get_title(soup):
            try:
                title = '\n'.join(link.extract().get_text().lower() for link in soup('title'))
                title = clear_text(title)
            except:
                title = []
            return title

        def get_body(soup):
            try:
                body = soup.getText()
                body = clear_text(body)
            except:
                body = []
            return body

        def get_h1(soup):
            try:
                h1 = '\n'.join(x.text for x in soup.findAll('h1'))
                h1 = clear_text(h1)
            except:
                h1 = []
            return h1

        def get_h2(soup):
            try:
                h2 = '\n'.join(x.text for x in soup.findAll('h2'))
                h2 = clear_text(h2)
            except:
                h2 = []
            return h2

        def get_h3(soup):
            try:
                h3 = '\n'.join(x.text for x in soup.findAll('h3'))
                h3 = clear_text(h3)
            except:
                h3 = []
            return h3

        def get_keywords(soup):
            try:
                keywords = '\n'.join(tag.attrs['content'] for tag in soup('meta') if
                                     'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['keywords'])
                keywords = clear_text(keywords)
            except:
                keywords = []
            return keywords

        def get_description(soup):
            try:
                description = '\n'.join(tag.attrs['content'] for tag in soup('meta') if
                                        'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in [
                                            'description'])
                description = clear_text(description)
            except:
                description = []
            return description

        links = get_a(soup)
        title = get_title(soup)
        body = get_body(soup)
        h1 = get_h1(soup)
        h2 = get_h2(soup)
        h3 = get_h3(soup)
        keywords = get_keywords(soup)
        description = get_description(soup)
        return links, title, body, h1, h2, h3, keywords, description



