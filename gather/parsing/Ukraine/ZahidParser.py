import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from text.StringCleaner import StringCleaner


class ZahidParser:

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

            ex_classes = doc.find_class('title')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            ex_classes = doc.find_class('desc')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            ex_classes = doc.get_element_by_id('newsSummary')
            for par in ex_classes:
                article_text += "\n"+par.text_content()
        except Exception as e:
            message = self.logger.make_message_link("ZahidParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = ZahidParser(logger)
    # success, article = my_parser.parse('https://zaxid.net'
    #                                    '/kerivnitstvo_dsns_vibachilos_pered_33_richnoyu_lvivyankoyu_'
    #                                    'za_vidmovu_u_sluzhbi_cherez_yiyi_stat_n1474844')
    success, article = my_parser.parse('https://zaxid.net'
                                       '/u_kiyevi_zlochinets_vipadkovo_vistriliv_oko_chotiririchniy_ditini_n1474869')
    print(article)
