import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class NewsgeParser:

    def __init__(self, app_loger):
        self.logger = app_loger

    def parse(self, url):
        try:
            headers = RequestHeaderGenerator.get_headers()
            request = Request(url, headers=headers)
            content = urllib.request.urlopen(request).read().strip().decode(errors='replace')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            if len(doc.find_class('entry-title blog-entry-title')) != 0:

                ex_classes = doc.find_class('entry-title blog-entry-title')
                par = ex_classes[0]
                article_text += "\n"+par.text_content()

                ex_classes = doc.find_class('entry-summary clearfix')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        all_p = par.findall("p")
                        if all_p:
                            for r in all_p:
                                article_text += "\n"+r.text_content()

            elif len(doc.find_class('entry-title post-title')) != 0:
                ex_classes = doc.find_class('entry-title post-title')
                par = ex_classes[0]
                article_text += par.text_content()+"\n"

                ex_classes = doc.find_class('entry-content entry')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        all_p = par.findall("p")
                        if all_p:
                            for r in all_p:
                                article_text += "\n"+r.text_content()

        except Exception as e:
            message = self.logger.make_message_link("NewsgeParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = NewsgeParser(logger)

    # success, article = my_parser.parse('https://news.ge/samushao-pirobebis-gaumjobeseba/')
    # success, article = my_parser.parse('https://news.ge/dzalian-mnishvnelovani-punktebia-rusetis-charevaze/')
    # success, article = my_parser.parse('https://news.ge/2019/08/09/galaxy-note10-samsung/')
    succes, article = my_parser.parse('https://news.ge/2019/08/09/ra-uziandeba-hover-bords/')
    print(article)
