import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class IpressuaParser:

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

            ex_classes = doc.find_class('readheader')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            element = doc.get_element_by_id('lead')
            article_text += "\n" + element.text_content()

            ex_classes = doc.find_class('bodylinkchange')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            message = self.logger.make_message_link("IpressuaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = IpressuaParser(logger)
    success, article = my_parser.parse('https://ipress.ua/articles'
                                       '/otse_hepiend_bude_yakshcho_ya_strybnu_z_7_poverhu_veteranka_oksana'
                                       '_yakubova_pro_borotbu_z_ptsr_281374.html')
    # success, article = my_parser.parse('https://ipress.ua/articles/na_zahysti_prav_lyudyny_284449.html')
    # success, article = my_parser.parse('https://interfax.com.ua/news/general/562562.html')
    print(article)
