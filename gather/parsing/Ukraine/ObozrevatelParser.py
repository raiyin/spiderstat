import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class ObozrevatelParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:
            headers = RequestHeaderGenerator.get_headers()
            request = Request(url, headers=headers)
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            classes = doc.find_class('news-full__title')
            if len(classes) != 0:
                e = classes[0]
                article_text += e.text_content()

                ex_classes = doc.find_class('news-full__text io-article-body')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        all_p = par.findall("p")
                        if all_p:
                            for r in all_p[:-2]:
                                article_text += "\n" + r.text_content()
            elif len(doc.find_class('news-video-full__header')) > 0:
                classes = doc.find_class('news-video-full__header')
                e = classes[0]
                all_p = e.findall("h1")
                if all_p:
                    for r in all_p:
                        article_text += "\n" + r.text_content()

                ex_classes = doc.find_class('news-video-full__text')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        all_p = par.findall("p")
                        if all_p:
                            for r in all_p[:-1]:
                                article_text += "\n" + r.text_content()

        except Exception as e:
            message = self.logger.make_message_link("ObozrevatelParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = ObozrevatelParser(logger)
    # success, article = my_parser.parse('https://www.obozrevatel.com/kiyany/crime/v-kieve-nochyu-rasstrelyali-dvuh
    # -chelovek-chto-izvestno.htm')
    success, article = my_parser.parse('https://www.obozrevatel.com/sport/sport/nokaut-pervyim-udarom-emelyanenko'
                                       '-pozorno-proigral-chempionskij-boj.htm')

    # success, article = my_parser.parse(
    #    'https://www.obozrevatel.com/tv/skandalnyij-drug-zelenskogo-snova-vsplyil-na-rostv.htm')
    print(article)
