import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea import FakeTestLogger
from miscellanea.StringCleaner import StringCleaner


class NewsdayazParser:

    def __init__(self, logger):
        self.logger = logger

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/" + str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('caption')

            if len(ex_classes) != 0:
                par = ex_classes[0]
                article_text += par.text_content()

                ex_classes = doc.find_class('description')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        all_p = par.findall("p")
                        if all_p:
                            for r in all_p:
                                article_text += "\n" + r.text_content()

            elif len(doc.find_class('post_title')) != 0:
                ex_classes = doc.find_class('post_title')
                par = ex_classes[0]
                article_text += par.text_content()

                ex_classes = doc.find_class('post_content')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        all_p = par.findall("p")
                        if all_p:
                            for r in all_p:
                                article_text += "\n" + r.text_content()

            elif len(doc.find_class('article-title')) != 0:
                # get title
                ex_classes = doc.find_class('article-title')
                par = ex_classes[0]
                article_text += par.text_content()
                article_text += "\n"

                # get article body
                ex_classes = doc.find_class('article-body')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        all_p = par.findall("p")
                        if all_p:
                            for r in all_p:
                                article_text += "\n" + r.text_content()

        except Exception as e:
            message = self.logger.make_message("NewsdayazParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = NewsdayazParser(logger)
    # success, article = my_parser.parse('https://news.day.az/world/1093356.html')
    # success, article = my_parser.parse('https://lady.day.az/news/guests/1104904.html')
    # success, article = my_parser.parse('https://lady.day.az/news/career/1107195.html')
    #success, article = my_parser.parse('https://news.day.az/azerinews/1146101.html')
    success, article = my_parser.parse('https://news.day.az/sport/1146098.html')
    print(article)
