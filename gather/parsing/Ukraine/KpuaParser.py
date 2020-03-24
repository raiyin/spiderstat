import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class KpuaParser:

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

            ex_classes = doc.find_class('content-img')

            if len(ex_classes) != 0:
                e = ex_classes.pop()
                r = e.findall("img")[0]
                article_text += str(r.xpath('//img/@alt')[1])
            else:
                ex_classes = doc.find_class('content-title')
                article_text += ex_classes[0].text_content()

            ex_classes = doc.find_class('content')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                r = e.findall("p")
                for par in r:
                    article_text += par.text_content()
            else:
                return 0, ""
        except Exception as e:
            message = self.logger.make_message_link("KpuaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = KpuaParser(logger)
    success, article = my_parser.parse('https://kp.ua/culture/629471-pevytsa-yulyia-'
                                       'savycheva-poteriala-pervoho-rebenka')
    # success, article = my_parser.parse('https://kp.ua/politics/633879/')
    print(article)
