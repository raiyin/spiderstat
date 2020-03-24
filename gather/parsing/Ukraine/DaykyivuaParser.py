import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class DaykyivuaParser:

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

            ex_classes = doc.find_class('title')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            ex_classes = doc.find_class('field-item even')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
                    all_p = par.findall("div/p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
                    all_p = par.findall("div/div/p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
                    all_p = par.findall("div/div/div/p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message_link("DaykyivuaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = DaykyivuaParser(logger)
    # success, article = my_parser.parse('http://day.kyiv.ua/uk/news/030219-zdiysnylasya-mriya-bagatoh-pokolin'
    #                                    '-pravoslavnyh-ukrayinciv-patriarh-filaret')
    success, article = my_parser.parse('http://day.kyiv.ua/uk/news/030219-ukrayinska-kondyterska-kompaniya-pid'
                                       '-brendom-disney-planuye-perekonaty-ditey-obyraty')
    print(article)
