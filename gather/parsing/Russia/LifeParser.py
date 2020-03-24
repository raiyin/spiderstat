import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class LifeParser:

    content = ""

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:
            article_text = ""
            headers = RequestHeaderGenerator.get_headers()
            request = Request(url, headers=headers)
            content = urllib.request.urlopen(request).read()

            doc = fromstring(content)
            doc.make_links_absolute(url)

            # Заголовок, если он есть.
            ex_classes = doc.find_class('post-page-header')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                r = e.findall("h1")
                for par in r:
                    # Красивая проверка, что строка не пустая
                    if par.text_content():
                        article_text += "\n" + par.text_content()

                # Текст новости
                e = doc.find_class('content-note').pop()
                r = e.findall("p")
                for par in r:
                    # Красивая проверка, что строка не пустая.
                    if par.text_content():
                        article_text += "\n" + par.text_content()

        except Exception:
            try:
                # Возможно, другой тип статьи
                doc = fromstring(content)  # .decode('utf-8'))
                doc.make_links_absolute(url)
                ex_classes = doc.find_class('longreads-subtitle')
                if len(ex_classes) != 0:
                    e = ex_classes.pop()
                    article_text += e.text_content()

                # Текст новости
                ex_classes = doc.find_class('content-note')
                if len(ex_classes) != 0:
                    e = ex_classes.pop()
                    r = e.findall("p")
                    for par in r:
                        # Красивая проверка, что строка не пустая.
                        if par.text_content():
                            article_text += "\n" + par.text_content()

                article_text = StringCleaner.clean(article_text)
                return 1, article_text

            except Exception as e:
                message = self.logger.make_message_link("LifeParser", e, url)
                self.logger.write_message(message)
                return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = LifeParser(logger)
    success, article = my_parser.parse('https://life.ru/t/новости/1202443/avakov_rasskazal_o_konfliktie_s_poroshienko')
    print(article)
