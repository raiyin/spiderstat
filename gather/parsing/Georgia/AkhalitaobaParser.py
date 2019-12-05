import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from text.StringCleaner import StringCleaner


class AkhalitaobaParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('entry-title')
            par = ex_classes[0]
            article_text += par.text_content()

            ex_classes = doc.find_class('entry-content cf')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message("AkhalitaobaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = AkhalitaobaParser(logger)
    # success, article = my_parser.parse('http://akhalitaoba.ge/2019/02/5-gasrola-da-2-datchrili-thamarashvilze-erth
    # -erthis-mdgomareoba-mdzimea/')
    success, article = my_parser.parse('http://akhalitaoba.ge/2019/02/thu-vinmes-unda-umravlesobis-datoveba-kari'
                                       '-ghiaa-da-sheudzlia-datovos-kaladze/')
    print(article)
