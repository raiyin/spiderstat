import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
import zlib
from miscellanea.logging import FakeTestLogger
from text.StringCleaner import StringCleaner


class RegnumruParser:

    def __init__(self, logger):
        self.logger = logger

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            data = urllib.request.urlopen(request, timeout=80).read()
            content = zlib.decompressobj(16+zlib.MAX_WBITS).decompress(data).decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('article-header')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            ex_classes = doc.find_class('article-text')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message_link("RegnumParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    fake_logger = FakeTestLogger.FakeTestLogger()
    my_parser = RegnumruParser(fake_logger)
    # success, article = my_parser.parse('https://regnum.ru/news/polit/2608206.html')
    # success, article = my_parser.parse('https://regnum.ru/news/cultura/2576301.html')
    success, article = my_parser.parse('https://regnum.ru/news/polit/2666592.html')
    print(article)
