import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from miscellanea.logging import FakeTestLogger
from text.StringCleaner import StringCleaner
from random import randint


class DialoguaParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:
            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)

            article_text = ""

            # header.
            ex_classes = doc.find_class('news-h')[0]
            # tag = ex_classes.findall('h1')[0]
            article_text += ex_classes.text_content()+"\n"

            # par = doc.find_class('news-text')[0]
            # article_text += '\n'+par.text_content()

            ex_classes = doc.find_class('news-text')
            if len(ex_classes) != 0:
                for i in range(len(ex_classes)):  # par in ex_classes:
                    if i == 0:
                        article_text += ex_classes[i].text_content() + "\n"
                    else:
                        all_p = ex_classes[i].findall("p")
                        if all_p:
                            for r in all_p:
                                article_text += "\n" + r.text_content()
        except Exception as e:
            message = self.logger.make_message_link("DialoguaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = DialoguaParser(logger)
    success, article = my_parser.parse('https://www.dialog.ua/ukraine/196153_1575632234')
    # success, article = my_parser.parse('https://www.dialog.ua/war/170677_1548841514')
    # success, article = my_parser.parse('https://www.dialog.ua/ukraine/175906_1554899454')
    print(article)
