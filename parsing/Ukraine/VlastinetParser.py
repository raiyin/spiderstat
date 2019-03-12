import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea import FakeTestLogger


class VlastinetParser:

    def __init__(self, logger):
        self.logger = logger

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('width664')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("h2")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()

            ex_classes = doc.find_class('newslid')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            ex_classes = doc.find_class('newsbig')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message("VlastinetParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger('', '', 'smtp.yandex.ru', 465)
    my_parser = VlastinetParser(logger)
    #success, article = my_parser.parse('http://vlasti.net/news/293576')
    success, article = my_parser.parse('http://vlasti.net/news/293573')
    print(article)
