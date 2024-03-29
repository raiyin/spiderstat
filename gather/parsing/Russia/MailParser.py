import urllib.request
from lxml.html import fromstring
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner


class MailParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:
            article_text = ""
            content = urllib.request.urlopen(url).read()
            doc = fromstring(content)  # .decode('utf-8'))
            doc.make_links_absolute(url)

            # Заголовок
            ex_classes = doc.find_class('hdr hdr_collapse hdr_bold_huge hdr_lowercase')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                article_text += e.text_content()
                e = doc.find_class('article__intro').pop()
                article_text += "\n" + e.text_content()

                # Текст новости
                e = doc.find_class('article__item article__item_alignment_left article__item_html')
                for par in e:
                    # Красивая проверка на непустоту списка
                    all_p = par.findall("p")
                    if all_p:
                        r = all_p.pop()
                        article_text += "\n" + r.text_content()
            else:
                return 0, ""

        except Exception as e:
            message = self.logger.make_message_link("MailParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = MailParser(logger)
    success, article = my_parser.parse('https://news.mail.ru/society/35093981/')
    print(article)
