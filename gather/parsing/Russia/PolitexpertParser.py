import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class PolitexpertParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:
            headers = RequestHeaderGenerator.get_headers()
            request = Request(url, headers=headers)
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)

            ex_classes = doc.find_class('js-mediator-article')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                r = e.findall("p")
                article_text = ""
                for par in r[:-1]:
                    article_text += "\n" + par.text_content()
            else:
                return 0, ""
        except Exception as e:
            message = self.logger.make_message_link("PolitexpertParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = PolitexpertParser(logger)
    success, article = my_parser.parse('https://politexpert.net/139050-venesuela-prodolzhit-prodavat-neft-ssha-maduro')
    # success, article = my_parser.parse('https://politexpert.net/139048-nad-alpami-turisticheskii-samolet
    # -stolknulsya-s-vertoletom-est-pogibshie')
    print(article)
