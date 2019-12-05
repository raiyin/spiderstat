from urllib.request import Request
from lxml.html import fromstring
from miscellanea.logging import FakeTestLogger
from text.StringCleaner import StringCleaner


class DialoguaParser:

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

            ex_classes = doc.find_class('news-news clearfix')[0]
            tag = ex_classes.findall('h1')[0]
            article_text += tag.text_content()

            par = doc.find_class('news-text')[0]
            article_text += '\n'+par.text_content()

            ex_classes = doc.find_class('news-text')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n" + r.text_content()
        except Exception as e:
            message = self.logger.make_message("DialoguaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = DialoguaParser(logger)
    success, article = my_parser.parse('https://www.dialog.ua/ukraine/170684_1548847344')
    # success, article = my_parser.parse('https://www.dialog.ua/war/170677_1548841514')
    # success, article = my_parser.parse('https://www.dialog.ua/ukraine/175906_1554899454')
    print(article)
