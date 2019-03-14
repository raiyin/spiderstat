import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea import FakeTestLogger
from miscellanea.StringCleaner import StringCleaner


class EuronewsgeParser:

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

            ex_classes = doc.find_class('entry-title')
            par = ex_classes[0]
            article_text += par.text_content()

            ex_classes = doc.find_class('td-post-content td-pb-padding-side')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message("EuronewsgeParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger('', '', 'smtp.yandex.ru', 465)
    my_parser = EuronewsgeParser(logger)
    #success, article = my_parser.parse('http://euronews.ge/%e1%83%96%e1%83%90%e1%83%a3%e1%83%a0-%e1%83%9c%e1%83%90%e1'
    #                                   '%83%ad%e1%83%a7%e1%83%94%e1%83%91%e1%83%98%e1%83%90-%e1%83%9b%e1%83%98%e1%83'
    #                                   '%a8%e1%83%90%e1%83%a1-%e1%83%a8%e1%83%94%e1%83%9b%e1%83%9d/')
    success, article = my_parser.parse('http://euronews.ge/%e1%83%a9%e1%83%a3%e1%83%a5%e1%83%93%e1%83%94%e1%83%91%e1'
                                       '%83%90-%e1%83%a5%e1%83%90%e1%83%a0%e1%83%97%e1%83%a3%e1%83%9a%e1%83%98-%e1%83'
                                       '%9c%e1%83%90%e1%83%92%e1%83%90%e1%83%96%e1%83%98-%e1%83%a1/')
    print(article)
