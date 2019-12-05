import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from text.StringCleaner import StringCleaner


class OneonetwoParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/" + str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
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
            message = self.logger.make_message("OneonetwoParser", e, url)
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
    success, article = my_parser.parse('https://112.ua/glavnye-novosti/gladkovskiy-vyshel-iz-sizo-posle-vneseniya'
                                       '-zaloga-v-106-mln-griven-511898.html')
    # success, article = my_parser.parse(
    #     'https://tv.112.ua/112_minut/utrennee-shou-112-minut-vypusk-ot-28032019-485689.html')
    print(article)
