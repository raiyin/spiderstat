import urllib.request
from lxml.html import fromstring
from miscellanea import FakeTestLogger
from miscellanea.StringCleaner import StringCleaner


class RbcParser:

    def __init__(self, logger):
        self.logger = logger

    def parse(self, url):
        try:
            article_text = ""
            content = urllib.request.urlopen(url).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)

            # Заголовок
            ex_classes = doc.find_class('article__header__title')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                article_text += e.text_content()

                # Текст новости
                e = doc.find_class('article__text').pop()
                r = e.findall("p")
                for par in r:
                    article_text += "\n" + par.text_content()
            else:
                return 0, ""

        except Exception as e:
            message = self.logger.make_message("RbcParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger('', '', 'smtp.yandex.ru', 465)
    my_parser = RbcParser(logger)
    success, article = my_parser.parse('https://www.rbc.ru/rbcfreenews/5bc8acd19a7947257ed65f69')
    print(article)
