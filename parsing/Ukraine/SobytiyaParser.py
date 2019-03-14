import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea import FakeTestLogger
from miscellanea.StringCleaner import StringCleaner


class SobitiyaParser:

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

            ex_classes = doc.find_class('publicFull')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("h1/b")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()

            ex_classes = doc.find_class('text')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("index/p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message("SobitiyaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger('', '', 'smtp.yandex.ru', 465)
    my_parser = SobitiyaParser(logger)
    #success, article = my_parser.parse('http://www.sobytiya.info/news/u-beregov-kryma-gremeli-vystrely')
    success, article = my_parser.parse('http://www.sobytiya.info/news/propavshiy-bez-vesti-kapitan-krymskogo-sudna'
                                       '-mog-pokinut-ukrainu-advokat')
    print(article)
