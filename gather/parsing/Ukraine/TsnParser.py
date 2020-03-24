import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class TsnParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:
            headers = RequestHeaderGenerator.get_headers()
            request = Request(url, headers=headers)
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('p-name c-post-title u-uppercase')[0]
            article_text += ex_classes.text_content()

            ex_classes = doc.find_class('p-summary c-post-lead')[0]
            article_text += '\n' + ex_classes.text_content()

            ex_classes = doc.find_class('e-content')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n" + r.text_content()
        except Exception as e:
            message = self.logger.make_message_link("TsnParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = TsnParser(logger)
    # success, article = my_parser.parse('https://tsn.ua/svit/u-siriyi-naymanci-rf-ta-iranu-vlashtuvali-mizh-soboyu'
    #                                    '-perestrilku-zmi-1286781.html')
    success, article = my_parser.parse('https://tsn.ua/ato/zvilneniy-pracivnik-doneckogo-viyskkomatu-perebravsya-v'
                                       '-ordlo-1317834.html?utm_source=page&utm_medium=lastnews')
    # success, article = my_parser.parse('https://tsn.ua/ukrayina/na-odeschini-splyundruvali-memorial-voyinam-unr-za'
    #                                    '-informaciyu-pro-zlochinciv-obicyayut-vinagorodu-1313817.html')
    print(article)
