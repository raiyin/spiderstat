import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea import FakeTestLogger


class IzParser:

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

            ex_classes = doc.find_class('text-article__inside')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                r = e.findall("div/div/p")
                article_text = ""
                for par in r:
                    article_text += "\n" + par.text_content()
            else:
                return 0, ""
        except Exception as e:
            message = self.logger.make_message("IzParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger('', '', 'smtp.yandex.ru', 465)
    my_parser = IzParser(logger)
    # success, article = my_parser.parse('https://iz.ru/805117/georgii-oltarzhevskii/vzryv-pokrovov-kto-podorval-linkor-novorossiisk')
    success, article = my_parser.parse('https://iz.ru/808585/2018-11-05/dva-zdaniia-obrushilis-v-tcentre-marselia')
    print(article)
