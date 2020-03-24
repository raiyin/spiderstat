import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class MusavatcomParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:
            headers = RequestHeaderGenerator.get_headers()
            request = Request(url, headers=headers)
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('news-content')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("h2")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
                    all_p = par.findall("div/p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message_link("MusavatcomParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = MusavatcomParser(logger)
    # success, article = my_parser.parse('http://musavat.com/news/obnarodovany-kadry-ispytanij-rossijskogo-tanka-t
    # -90ms-video_592734.html')
    success, article = my_parser.parse('http://musavat.com/news/po-iniciative-mehriban-alievoj-dan-ehsan-v-gyandzhe'
                                       '-foto_592756.html')
    print(article)
