from urllib.request import Request
from lxml.html import fromstring
from miscellanea.logging import FakeTestLogger
from text.StringCleaner import StringCleaner


class GazetaUaParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:

            s = Request.Session()
            s.trust_env = False
            response = s.get(url)
            content = response.read()

            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('w double article')
            if len(ex_classes) != 0:
                e = ex_classes[0]
                r = e.findall('article/h1')
                article_text += r[0].text_content()

            ex_classes = doc.find_class('article-content clearfix')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                r = e.findall("article/p")
                for par in r[:-2]:
                    article_text += "\n" + par.text_content()
            else:
                return 0, ""
        except Exception as e:
            message = self.logger.make_message_link("GazetaUaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = GazetaUaParser(logger)
    success, article = my_parser.parse('https://gazeta.ua/articles/donbas/_u-hmelnickomu-zhorstoko-pokarali'
                                       '-separatistku/882529')
    # success, article = my_parser.parse('https://gazeta.ua/articles/world-life/_litaki-rf-ta-ssa-zchepilisya-v-nebi'
    #                                    '-nad-evropoyu/882530')
    print(article)
