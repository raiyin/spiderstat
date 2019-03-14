import urllib.request
from lxml.html import fromstring
from miscellanea import FakeTestLogger
from miscellanea.StringCleaner import StringCleaner


class BbcParser:

    def __init__(self, logger):
        self.logger = logger

    def parse(self, url):
        try:
            article_text = ""
            content = urllib.request.urlopen(url).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)

            # Главный абзац новости
            ex_classes = doc.find_class('story-body__h1')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                article_text += e.text_content().strip()

                # Текст новости
                e = doc.find_class('story-body__inner').pop()
                r = e.findall("p")
                for par in r:
                    text = par.text_content().strip()
                    if text:
                        article_text += "\n" + text
            elif len(doc.find_class('vxp-media__headline')) != 0:
                ex_classes = doc.find_class('vxp-media__headline')
                e = ex_classes.pop()
                article_text += e.text_content().strip()

                # Текст новости
                e = doc.find_class('vxp-media__summary').pop()
                r = e.findall("p")
                for par in r:
                    text = par.text_content().strip()
                    if text:
                        article_text += "\n" + text
            else:
                return 0, ""

        except Exception as e:
            message = self.logger.make_message("BbcParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger('', '', 'smtp.yandex.ru', 465)
    my_parser = BbcParser(logger)
    success, article = my_parser.parse('https://www.bbc.com/russian/features-46067230')
    # success, article = my_parser.parse('https://www.bbc.com/russian/av/media-45904959')

    print(article)
