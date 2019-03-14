import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea import FakeTestLogger
from miscellanea.StringCleaner import StringCleaner


class ApsnygeParser:

    def __init__(self, logger):
        self.logger = logger

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
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
            message = self.logger.make_message("ApsnygeParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger('', '', 'smtp.yandex.ru', 465)
    my_parser = ApsnygeParser(logger)
    #success, article = my_parser.parse('https://www.apsny.ge/2019/pol/1549427079.php')
    success, article = my_parser.parse('https://www.apsny.ge/2019/eco/1549427740.php')
    print(article)
