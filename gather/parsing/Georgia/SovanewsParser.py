import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from text.StringCleaner import StringCleaner


class SovanewsParser:

    def __init__(self, app_loger):
        self.logger = app_loger

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/" + str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('mvp-post-title entry-title')
            if len(ex_classes) != 0:
                par = ex_classes[0]
                article_text += "\n" + par.text_content()

                ex_classes = doc.find_class('left relative')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        all_p = par.findall("section/p")
                        if all_p:
                            for r in all_p:
                                article_text += "\n" + r.text_content()
            elif len(doc.find_class('mvp-post-excerpt')) != 0:
                ex_classes = doc.find_class('mvp-post-excerpt')
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n" + r.text_content()
            elif len(doc.find_class('mvp-post-content-in')) != 0:
                ex_classes = doc.find_class('mvp-post-content-in')
                for par in ex_classes:
                    all_p = par.findall("div/section/p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n" + r.text_content()
        except Exception as e:
            message = self.logger.make_message_link("SovanewsParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = SovanewsParser(logger)
    # success, article = my_parser.parse('https://sova.news/2019/02/08/grazhdane-gruzii-i-ukrainy-budut-ezdit-drug-k'
    #                                    '-drugu-po-id-kartam/')
    success, article = my_parser.parse('https://sova.news/2019/12/05/nigilizm-v-obshhestve-horoshaya-pochva-dlya-dezinformatsii-i-propagandy/')
    print(article)
