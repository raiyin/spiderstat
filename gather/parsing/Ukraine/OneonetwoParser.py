import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator
import zlib


class OneonetwoParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:
            content = ""
            headers = RequestHeaderGenerator.get_headers()
            request = Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            if response.info().get('Content-Encoding') == 'gzip':
                buf = response.read()
                data = zlib.decompress(buf, 16 + zlib.MAX_WBITS)
                content = data.decode('utf-8')
            else:
                content = response.read().decode('utf-8')

            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            e = doc.find_class('h1')
            if len(e) != 0:
                e = e[0]
                article_text += e.text_content()

                e = doc.find_class('top-text')[0]
                article_text += e.text_content()

                ex_classes = doc.find_class('article-content_text')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        all_p = par.findall("p")
                        if all_p:
                            for r in all_p:
                                article_text += "\n" + r.text_content()
            elif len(doc.find_class('b-center-item-head-info')) != 0:
                e = doc.find_class('b-center-item-head-info')[0]
                for par in e:
                    article_text += "\n" + par.text_content()
        except Exception as e:
            message = self.logger.make_message_link("OneonetwoParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = OneonetwoParser(logger)
    # success, article = my_parser.parse('https://112.ua/obshchestvo/opasnost-3-go-urovnya-goschs-preduprezhdaet'
    #                                    '-turistov-ob-ugroze-shoda-lavin-v-gorah-zakarpatskoy-oblasti-478389.html')
    # success, article = my_parser.parse('https://112.ua/avarii-chp/dva-goroda-v-lnr-ostalis-bez-vody-478390.html')
    success, article = my_parser.parse(
        'https://112.ua/ekonomika/cena-na-zoloto-dostigla-maksimuma-za-poslednie-vosem-let-528536.html')
    # success, article = my_parser.parse(
    #     'https://tv.112.ua/112_minut/utrennee-shou-112-minut-vypusk-ot-28032019-485689.html')
    print(article)
