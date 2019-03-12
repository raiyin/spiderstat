import urllib.request
from urllib.request import Request
from random import randint
from bs4 import BeautifulSoup
from miscellanea import FakeTestLogger


class FactycomuaParser:

    def __init__(self, logger):
        self.logger = logger

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/" + str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
            soup = BeautifulSoup(content, 'html5lib')

            article_text = ""

            paragraphs = soup.findAll("h1")
            for element in paragraphs:
                article_text += "\n" + str(element.text)

            paragraphs = soup.findAll("div", {"class": "kv-post-content-text"})
            for element in paragraphs:
                for el in element:
                    if hasattr(el, "text") & hasattr(el, "name"):
                        if el.name == 'p':
                            article_text += "\n" + str(el.text)
        except Exception as e:
            message = self.logger.make_message("FactycomuaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger('', '', 'smtp.yandex.ru', 465)
    my_parser = FactycomuaParser(logger)
    #success, article = my_parser.parse('https://fakty.com.ua/ua/proisshestvija/20190203-pozhezha-na-lisovij-ye'
    #                                   '-zagroza-obvalu-konstruktsij/')
    success, article = my_parser.parse('https://fakty.com.ua/ua/ukraine/20190203-vybory-2019-poroshenko-podav'
                                       '-dokumenty-u-tsvk/')
    print(article)
