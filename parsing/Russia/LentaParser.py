import urllib.request
from lxml.html import fromstring
from miscellanea import FakeTestLogger
from miscellanea.StringCleaner import StringCleaner


class LentaParser:

    def __init__(self, logger):
        self.logger = logger

    def parse(self, url):
        try:
            article_text = ""
            content = urllib.request.urlopen(url).read()
            doc = fromstring(content.decode('utf-8'))
            doc.make_links_absolute(url)

            # Заголовок
            ex_classes = doc.find_class('b-topic__title')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                article_text += e.text_content()

                # Текст новости
                e = doc.find_class('b-text clearfix js-topic__text').pop()
                r = e.findall("p")
                for par in r:
                    article_text += "\n" + par.text_content()
            else:
                return 0, ""
        except Exception as e:
            message = self.logger.make_message("LentaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger('', '', 'smtp.yandex.ru', 465)
    my_parser = LentaParser(logger)
    success, article = my_parser.parse('https://lenta.ru/news/2018/10/18/40n6/')
    print(article)
