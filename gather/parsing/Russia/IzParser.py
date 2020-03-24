from lxml.html import fromstring
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
import requests


class IzParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:
            content = requests.get(url).text

            doc = fromstring(content)
            doc.make_links_absolute(url)

            ex_classes = doc.find_class('text-article__inside')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                r = e.findall("div/div/p")
                article_text = ""
                for par in r:
                    article_text += "\n" + par.text_content()
            else:
                return 0, ""
        except Exception as e:
            message = self.logger.make_message_link("IzParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = IzParser(logger)
    # success, article = my_parser.parse('https://iz.ru/805117/georgii-oltarzhevskii/vzryv-pokrovov-kto-podorval
    # -linkor-novorossiisk') success, article = my_parser.parse(
    # 'https://iz.ru/808585/2018-11-05/dva-zdaniia-obrushilis-v-tcentre-marselia')
    success, article = my_parser.parse('https://iz.ru/860325/2019-03-25/vozbuzhdeno-delo-o-moshennichestve-na-1-mln'
                                       '-rublei-v-ogt-cheliabinska')
    print(article)
