import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from text.StringCleaner import StringCleaner


class VestiuaParser:

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

            element = doc.get_element_by_id('news-title')
            article_text += element.text_content()

            ex_classes = doc.find_class('post_content cf')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p[:-1]:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message_link("VestiuaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = VestiuaParser(logger)
    # success, article = my_parser.parse('https://vesti-ua.net/novosti/politika/95172-ne-to-pokazyval-skandal-v'
    #                                    '-rukovodstve-uapershiy.html')
    success, article = my_parser.parse('https://vesti-ua.net/novosti/zdorove/95174-dietologi-rasstroili-myasoedov'
                                       '-vazhnym-zayavleniem.html')
    print(article)
