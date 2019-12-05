import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from text.StringCleaner import StringCleaner


class NovostgeParser:

    def __init__(self, app_loger):
        self.logger = app_loger

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('entry-title')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            ex_classes = doc.find_class('entry-content')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message("NovostgeParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = NovostgeParser(logger)
    # success, article = my_parser.parse('http://novost.ge/2019/02/05/%d0%b2-%d0%bf%d0%be%d1%80%d1%82%d1%83-%d0%bf%d0'
    #                                    '%be%d1%82%d0%b8-%d0%b0%d0%bc%d0%b5%d1%80%d0%b8%d0%ba%d0%b0%d0%bd%d1%81%d0%ba'
    #                                    '%d0%b0%d1%8f-%d0%ba%d0%be%d1%80%d0%bf%d0%be%d1%80%d0%b0%d1%86%d0%b8%d1%8f/')
    success, article = my_parser.parse('http://novost.ge/2019/02/05/%d0%b3%d1%80%d1%83%d0%b7%d0%b8%d1%8f-%d0%bf%d0%be'
                                       '%d0%bf%d0%b0%d0%bb%d0%b0-%d0%b2-%d1%80%d0%b5%d0%b9%d1%82%d0%b8%d0%bd%d0%b3'
                                       '-%d0%ba%d1%80%d1%83%d0%bf%d0%bd%d0%b5%d0%b9%d1%88%d0%b8%d1%85-%d1%81%d1%82/')
    print(article)
