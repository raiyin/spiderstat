import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class ZnajParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:
            headers = RequestHeaderGenerator.get_headers()
            request = Request(url, headers=headers)
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            e = doc.find_class('getstat-article')[0]
            all_hone = e.findall('header/h1')[0]
            article_text += all_hone.text_content()

            ex_classes = doc.find_class('article-body')
            finded_class = ex_classes[0]
            all_p = finded_class.findall("p")
            for p in all_p:
                article_text += "\n" + p.text_content()
        except Exception as e:
            message = self.logger.make_message_link("ZnajParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = ZnajParser(logger)
    # success, article = my_parser.parse('https://znaj.ua/society/206327-privatbank-potrapiv-u-zhahliviy-skandal-z'
    #                                    '-vigadanimi-borgami-takih-shahrajiv-shche-poshukati-treba')
    # success, article = my_parser.parse('https://znaj.ua/society/206325-vchiteliv-zmusyat-zdavati-zno-de-i-koli')
    # success, article = my_parser.parse('https://znaj.ua/society/206340-fiziognomist-poyasnila-shcho-prihovuye-zelenskiy-uvaga-na-ochi-ta-nis')
    success, article = my_parser.parse('https://kyiv.znaj.ua/296839-u-kiyevi-zabitiy-pasazhirami-avtobus-vletiv-u-vantazhivku-postrazhdalo-ne-menshe-desyati-lyudey')
    print(article)
