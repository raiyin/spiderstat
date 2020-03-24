import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class KratkonewsParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:
            headers = RequestHeaderGenerator.get_headers()
            request = Request(url, headers=headers)
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('main-col pull-left')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("section/header/h1")
                    if all_p:
                        for r in all_p:
                            article_text += r.text_content()

            ex_classes = doc.find_class('entry-content clearfix')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message_link("KratkonewsParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = KratkonewsParser(logger)
    # success, article = my_parser.parse('http://kratko-news.com/2019/02/03/arnold-shvarcenegger-nachal-semki-v'
    #                                    '-terminatore-6-cherez-3-mesyaca-posle-operacii-na-serdce/')
    success, article = my_parser.parse('http://kratko-news.com/2019/02/03/elizabet-xerli-vyglyadit-sensacionno-v-svoi'
                                       '-53-goda/')
    print(article)
