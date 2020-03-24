import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class ApsnygeParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:
            headers = RequestHeaderGenerator.get_headers()
            request = Request(url, headers=headers)
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('article')
            par = ex_classes[0]
            article_text += par.text_content()

            ex_classes = doc.find_class('txt-item-news')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    article_text += '\n'+par.text_content()
        except Exception as e:
            message = self.logger.make_message_link("ApsnygeParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = ApsnygeParser(logger)
    # success, article = my_parser.parse('https://www.apsny.ge/2019/pol/1549427079.php')
    success, article = my_parser.parse('https://www.apsny.ge/2020/pol/1578442454.php')
    print(article)
