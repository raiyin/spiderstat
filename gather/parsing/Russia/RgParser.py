import urllib.request
from lxml.html import fromstring
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class RgParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:
            article_text = ""
            content = urllib.request.urlopen(url).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)

            # Главный абзац новости
            ex_classes = doc.find_class('b-material-wrapper__lead')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                article_text += e.text_content()

                # Текст новости
                e = doc.find_class('b-material-wrapper__text').pop()
                r = e.findall("p")
                for par in r:
                    article_text += "\n" + par.text_content()

            elif len(doc.find_class('b-material-head__title')) != 0:
                ex_classes = doc.find_class('b-material-head__title')
                e = ex_classes.pop()
                article_text += e.text_content()

                # Текст новости
                e = doc.find_class('b-material-wrapper__text').pop()
                r = e.findall("p")
                for par in r:
                    article_text += "\n" + par.text_content()
            else:
                return 0, ""
        except Exception as e:
            message = self.logger.make_message_link("RgParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = RgParser(logger)
    # success, article = my_parser.parse('https://rg.ru/2018/10/18/cb-nameren-otmenit-bankovskoe-rabstvo.html')
    success, article = my_parser.parse(
        'https://rg.ru/2018/10/30/sotni-avtomobilej-maserati-sgoreli-pri-pozhare-v-italii.html')

    print(article)
