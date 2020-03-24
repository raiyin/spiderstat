import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class SputnikgeorgiaParser:

    def __init__(self, app_loger):
        self.logger = app_loger

    def parse(self, url):
        try:
            headers = RequestHeaderGenerator.get_headers()
            request = Request(url, headers=headers)
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('b-article__header-title')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            ex_classes = doc.find_class('b-article__lead')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()

            ex_classes = doc.find_class('b-article__text')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message_link("SputnikgeorgiaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = SputnikgeorgiaParser(logger)
    # success, article = my_parser.parse('https://sputnik-georgia.ru/politics/20190205/244210530/Nam-vsem-pridetsya'
    #                                    '-idti-v-tyurmu---chto-ne-ponravilos-ministru-yustitsii-Gruzii.html')
    success, article = my_parser.parse('https://sputnik-georgia.ru/politics/20190205/244210809/Anri-Okhanashvili-stal'
                                       '-predsedatelem-yuridicheskogo-komiteta-parlamenta.html')
    print(article)
