import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea import FakeTestLogger
from miscellanea.StringCleaner import StringCleaner


class InfonineParser:

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

            ex_classes = doc.find_class('article_title')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            ex_classes = doc.find_class('article-content')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            #ex_classes = doc.find_class('article-content')
            #if len(ex_classes) != 0:
            #    for par in ex_classes:
            #        all_p = par.findall("p")
            #        if all_p:
            #            for r in all_p:
            #                article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message("InfonineParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger('', '', 'smtp.yandex.ru', 465)
    my_parser = InfonineParser(logger)
    #success, article = my_parser.parse('http://www.info9.ge/politika/203857-uzenaes-sasamarthloshi-dimitri'
    #                                   '-gvritishvilis-kandidaturas-chemi-mkhardatcera-ar-eqneba--thamar-chugoshvili'
    #                                   '.html?lang=ka-GE&utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A'
    #                                   '+info9+%28Info9.Ge%29&utm_content=FeedBurner')
    success, article = my_parser.parse('http://www.info9.ge/uckhoethi/203853-donald-tuski-adamianebisthvis-vinc'
                                       '-britaneths-samoqmedo-gegmis-gareshe-evrokavshiridan-gasvlisken-moutsodebda'
                                       '-jojokhethshi-calke-adgilia-gamoyofili.html?lang=ka-GE&utm_source=feedburner'
                                       '&utm_medium=feed&utm_campaign=Feed%3A+info9+%28Info9.Ge%29&utm_content'
                                       '=FeedBurner')
    print(article)
