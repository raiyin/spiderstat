import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class InfonineParser:

    def __init__(self, app_loger):
        self.logger = app_loger

    def parse(self, url):
        try:
            headers = RequestHeaderGenerator.get_headers()
            request = Request(url, headers=headers)
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('article_title')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            ex_classes = doc.find_class('article-content')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

        except Exception as e:
            message = self.logger.make_message_link("InfonineParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = InfonineParser(logger)
    success, article = my_parser.parse('http://www.info9.ge/politika/217075-giorgi-margvelashvili-opoziciuri-speqtri-gazrdilia-adre-gadadeqiq-iyo-sityva-romlithac-khelisuflebas-mivmarthavdith-dghes-ki-gaerthianebulia-ufro-mnishvnelovani-miznis-irgvliv.html?lang=ka-GE&utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+info9+%28Info9.Ge%29')
    #success, article = my_parser.parse('http://www.info9.ge/uckhoethi/203853-donald-tuski-adamianebisthvis-vinc'
    #                                   '-britaneths-samoqmedo-gegmis-gareshe-evrokavshiridan-gasvlisken-moutsodebda'
    #                                   '-jojokhethshi-calke-adgilia-gamoyofili.html?lang=ka-GE&utm_source=feedburner'
    #                                   '&utm_medium=feed&utm_campaign=Feed%3A+info9+%28Info9.Ge%29&utm_content'
    #                                   '=FeedBurner')
    print(article)
