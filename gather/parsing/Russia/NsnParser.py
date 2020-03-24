import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class NsnParser:

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

            e = doc.find_class('_2Qs6X zbp1k _3u1kh')[0]
            article_text += e.text_content()
            article_text += "\n"

            e = doc.find_class('K3msD _14oZN _3u1kh').pop()
            article_text += "\n" + e.text_content()
            article_text += "\n"

            ex_classes = doc.find_class('_3j3bx XUGFY _3u1kh')
            if len(ex_classes) != 0:
                for par in ex_classes[:]:
                    article_text += par.text_content()
        except Exception as e:
            message = self.logger.make_message_link("NsnParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = NsnParser(logger)
    # success, article = my_parser.parse('http://nsn.fm/hots/inflyaciya-v-venesuele-v-2019-godu-prevysit-10000000.html')
    success, article = my_parser.parse('https://nsn.fm/ukraine/geroi-ukrainy-hochet-stat-ministrom')
    print(article)
