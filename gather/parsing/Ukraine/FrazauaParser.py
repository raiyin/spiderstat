import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class FrazauaParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:
            headers = RequestHeaderGenerator.get_headers()
            request = Request(url, headers=headers)
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)

            ex_classes = doc.find_class('article__title article__title__big')
            par = ex_classes[0]
            article_text = par.text_content()

            ex_classes = doc.find_class('article__summary')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("div/p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message_link("FrazauaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = FrazauaParser(logger)
    # success, article = my_parser.parse('https://fraza.ua/video/275776'
    #                                    '-v_set_popalo_video_grandioznogo_proryva_damby_v_brazilii')
    success, article = my_parser.parse('https://fraza.ua/news/275775-suprugi-belovy-podlo-obmanuli-nikolaevskogo'
                                       '-strelka-bagirjantsa-smi')
    print(article)
