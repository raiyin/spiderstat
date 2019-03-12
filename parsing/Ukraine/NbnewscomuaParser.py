import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea import FakeTestLogger


class NbnewscomuaParser:

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

            ex_classes = doc.find_class('entry-header')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("h1")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()

            ex_classes = doc.find_class('entry-content')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message("NbnewscomuaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger('', '', 'smtp.yandex.ru', 465)
    my_parser = NbnewscomuaParser(logger)
    #success, article = my_parser.parse('https://nbnews.com.ua/za-rubezhom/2019/02/03/severnaia-koreia-vsled-za'
    #                                   '-rossiei-podderjala-madyro/')
    success, article = my_parser.parse('https://nbnews.com.ua/politika/2019/02/03/vybory-prezidenta-segodnia-yje-7'
                                       '-chelovek-prinesli-dokymenty-v-cik/')
    print(article)
