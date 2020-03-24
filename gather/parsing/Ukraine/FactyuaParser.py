import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from bs4 import BeautifulSoup
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class FactyuaParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:
            headers = RequestHeaderGenerator.get_headers()
            request = Request(url, headers=headers)
            content = urllib.request.urlopen(request).read().decode('utf-8')
            soup = BeautifulSoup(content, 'html5lib')
            doc = fromstring(content)

            article_text = ""

            e = doc.find_class('zag3')[0]
            article_text += e.text_content()

            paragraphs = soup.find(id='article_content3').find_all()[:-2]
            for element in paragraphs:
                article_text += str(element.text)
        except Exception as e:
            message = self.logger.make_message_link("FactyuaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = FactyuaParser(logger)
    # success, article = my_parser.parse('https://fakty.ua/294365-bud-ty-proklyata-vesna---2014-v-krymu-na-stende-s
    # -gazetami-razmestili-lyubopytnoe-obyavlenie')
    success, article = my_parser.parse('https://fakty.ua/294361-v-ukraine-vtroe-snizili-normy-potrebleniya-gaza-chto'
                                       '-budet-s-cenami-na-kommunalku')
    print(article)
