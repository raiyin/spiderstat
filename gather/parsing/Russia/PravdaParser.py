import urllib.request
from lxml.html import fromstring
from miscellanea.logging import FakeTestLogger
from text.StringCleaner import StringCleaner


class PravdaParser:

    def __init__(self, logger):
        self.logger = logger

    def parse(self, url):
        try:
            article_text = ""
            content = urllib.request.urlopen(url).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)

            # Главный абзац новости
            # e = doc.find_class('lead').pop()
            # article_text += e.text_content()

            # Текст новости
            ex_classes = doc.find_class('full article full-article')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                r = e.findall("p")
                for par in r:
                    article_text += "\n" + par.text_content()
            else:
                return 0, ""
        except Exception as e:
            message = self.logger.make_message_link("PravdaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger('', '', 'smtp.yandex.ru', 465)
    my_parser = PravdaParser(logger)
    success, article = my_parser.parse('https://zoo.pravda.ru/news/zoouseful/18-10-2018/1396417-birds-0/')
    print(article)
