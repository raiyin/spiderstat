import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from text.StringCleaner import StringCleaner


class TabulaParser:

    def __init__(self, app_loger):
        self.logger = app_loger

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            # Для статей, которые содержат в адресе  story
            ex_classes = doc.find_class('article-header')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("h1")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()

            ex_classes = doc.find_class('content-body')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()

            # Для статей, которые содержат в адресе verbatim
            ex_classes = doc.find_class('verbatim-header')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("h1")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()

            ex_classes = doc.find_class('text-content')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message_link("TabulaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = TabulaParser(logger)
    # success, article = my_parser.parse('http://www.tabula.ge/ge/story/143896-patriotebi-ukrainashi-msoflio-patriarqis'
    #                                    '-qmedebebi-calsaxd-uarkofitad-unda-shevafasot')
    success, article = my_parser.parse('http://www.tabula.ge/ge/verbatim/143897-tsulukiani-biltssitkvaoba-tu'
                                       '-sheizghuda-kvelas-mogvitsevs-tsavidet-cixeshi')
    print(article)
