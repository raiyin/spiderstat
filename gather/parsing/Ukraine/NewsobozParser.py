import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class NewsobozParser:

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

            ex_classes = doc.find_class('title-block')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            ex_classes = doc.find_class('pubBody _ga1_on_')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message_link("NewsobozParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = NewsobozParser(logger)
    # success, article = my_parser.parse('http://newsoboz.org/it_tehnologii/facebook-i-twitter-blokiruyut-akkaunty'
    # '-svyazannye-s-rf-venesueloy-01022019104431') success, article = my_parser.parse(
    # 'http://newsoboz.org/politika/posol-es-v-rossii-ustroil-demarsh-iz-za-ukrainy' '-01022019171600') success,
    # article = my_parser.parse('http://newsoboz.org/obshchestvo/kak-upotreblyat-kurkumu-chtoby-izbavitsya-ot-boli-v
    # -sustavah-02042019115900')
    success, article = my_parser.parse('http://newsoboz.org/proisshestviya/soobshchili-o-tsennoy-nahodke-na'
                                       '-pepelishche-pomestya-gontarevyh-17092019124702')
    print(article)
