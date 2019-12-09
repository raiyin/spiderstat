import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from text.StringCleaner import StringCleaner


class RtParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/" + str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            e = doc.find_class('article__heading article__heading_article-page')
            if len(e) != 0:
                e = e.pop()
                article_text += "\n" + e.text_content()

                e = doc.find_class('article__summary').pop()
                article_text += "\n" + e.text_content()

                ex_classes = doc.find_class('article__text article__text_article-page js-mediator-article')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        all_p = par.findall("p")
                        if all_p:
                            for r in all_p:
                                article_text += "\n" + r.text_content()
            elif len(doc.find_class('article__heading article__heading_videoclub')) != 0:
                e = doc.find_class('article__heading article__heading_videoclub').pop()
                article_text += "\n" + e.text_content()

                ex_classes = doc.find_class('article__summary js-mediator-article')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        article_text += "\n" + par.text_content()
            elif len(doc.find_class('article__heading')) != 0:
                e = doc.find_class('article__heading').pop()
                article_text += "\n" + e.text_content()

                ex_classes = doc.find_class('article__text js-mediator-article')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        article_text += "\n" + par.text_content()

        except Exception as e:
            message = self.logger.make_message_link("RtParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = RtParser(logger)
    # success, article = my_parser.parse('https://russian.rt.com/russia/news/596430-flot-armiya-rossiya?utm_source
    # =rss&utm_medium=rss&utm_campaign=RSS') success, article = my_parser.parse(
    # 'https://russian.rt.com/sport/article/596454-zagitova-chempionat-evropy?utm_source=rss&utm_medium=rss
    # &utm_campaign=RSS') success, article = my_parser.parse(
    # 'https://russian.rt.com/ussr/video/616123-kravchuk-maidan-vibori-ukraina-prezident?utm_source=rss&utm_medium
    # =rss&utm_campaign=RSS')
    success, article = my_parser.parse('https://russian.rt.com/opinion/617376-babickii-zelenskii-vybory-prezident'
                                       '-ukraina?utm_source=rss&utm_medium=rss&utm_campaign=RSS')
    print(article)
