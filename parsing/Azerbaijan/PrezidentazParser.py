import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea import FakeTestLogger
from miscellanea.StringCleaner import StringCleaner


class PrezidentazParser:

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

            ex_classes = doc.find_class('news_heading')
            if len(ex_classes)!=0:
                par = ex_classes[0]
                article_text += "\n"+par.text_content()

                ex_classes = doc.find_class('news_paragraph-block')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        all_p = par.findall("p")
                        if all_p:
                            for r in all_p:
                                article_text += "\n"+r.text_content()
            else:
                ex_classes = doc.find_class('letter_heading')
                par = ex_classes[0]
                article_text += "\n"+par.text_content()

                ex_classes = doc.find_class('letter_text-body')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        all_p = par.findall("p")
                        if all_p:
                            for r in all_p:
                                article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message("PrezidentazParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger('', '', 'smtp.yandex.ru', 465)
    my_parser = PrezidentazParser(logger)
    #success, article = my_parser.parse('https://ru.president.az/articles/31802')
    success, article = my_parser.parse('https://ru.president.az/articles/31807')
    #success, article = my_parser.parse('http://ru.president.az/articles/32429')
    print(article)
