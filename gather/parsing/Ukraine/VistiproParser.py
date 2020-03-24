import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class VistiproParser:

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

            ex_classes = doc.find_class('field field--name-title field--type-string')
            par = ex_classes[0]
            article_text += "\n" + par.text_content()

            ex_classes = doc.find_class('clearfix text-formatted field field--name-body field--type-text-with-summary '
                                        'field--label-hidden field__item')
            if len(ex_classes) != 0:
                for par in ex_classes[:-3]:
                    article_text += par.text_content()
        except Exception as e:
            message = self.logger.make_message_link("VistiproParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = VistiproParser(logger)
    success, article = my_parser.parse(
        'http://visti.pro/uk/ekonomika-ta-finansi/za-minuliy-rik-borgi-po-komunalci-virosli-na-23-mlrd-grn')
    # success, article = my_parser.parse('http://visti.pro/uk/podii/politvyaznyu-pavlu-gribu-viklikali-shvidku-pid
    # -chas-sudovogo-zasidannya')
    print(article)
