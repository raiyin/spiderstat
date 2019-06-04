import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea import FakeTestLogger
from miscellanea.StringCleaner import StringCleaner


class DialoguaParser:

    def __init__(self, logger):
        self.logger = logger

    def parse(self, url):
        try:

            #request = Request(url)

            #headers = {
            #    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" +
            #                  str(randint(40, 70)) + ".0.2227.0 Safari/537.36", 'Host': "www.dialog.ua",
            #    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            #    'Accept-Language': "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            #    'DNT': "1",
            #    'Connection': "keep-alive",
            #    'Cookie': "b=b; swp_token=1554922583:eb914d50115a1b16513a6e03f1034555:13a4a8a1366d72f545a3863c67365d87; PHPSESSID=7g3lebsa7tq4r7bkifge92gn8v",
            #    'Upgrade-Insecure-Requests': "1",
            #    'Cache-Control': "max-age=0"}

            #request.headers = headers
            #content = urllib.request.urlopen(request).read()
            #doc = fromstring(content)
            #doc.make_links_absolute(url)

            s = Request.Session()
            s.trust_env = False
            response = s.get(url)
            content = response.read()
            doc = fromstring(content)
            doc.make_links_absolute(url)

            article_text = ""

            ex_classes = doc.find_class('news-news clearfix')[0]
            tag = ex_classes.findall('h1')[0]
            article_text += tag.text_content()

            par = doc.find_class('news-text')[0]
            article_text += '\n'+par.text_content()

            ex_classes = doc.find_class('news-text')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n" + r.text_content()
        except Exception as e:
            message = self.logger.make_message("DialoguaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger('', '', 'smtp.yandex.ru', 465)
    my_parser = DialoguaParser(logger)
    success, article = my_parser.parse('https://www.dialog.ua/ukraine/170684_1548847344')
    #success, article = my_parser.parse('https://www.dialog.ua/war/170677_1548841514')
    #success, article = my_parser.parse('https://www.dialog.ua/ukraine/175906_1554899454')
    print(article)
