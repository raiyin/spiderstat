import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class RentvParser:

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

            e = doc.find_class('news clearfix')
            for par in e:
                # Красивая проверка на непустоту списка
                all_p = par.findall("h1")
                if all_p:
                    r = all_p.pop()
                    article_text += "\n" + r.text_content()

            article_text += "\n"
            ex_classes = doc.find_class('field-item even')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    article_text += "\n" + par.text_content()
        except Exception as e:
            message = self.logger.make_message_link("RentvParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = RentvParser(logger)
    # success, article = my_parser.parse('http://ren.tv/node/383290')
    success, article = my_parser.parse('http://ren.tv/node/383293')
    print(article)
