import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from miscellanea.RequestHeaderGenerator import RequestHeaderGenerator


class AifuaParser:

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

            # header
            ex_classes = doc.find_class('article')
            article_class = ex_classes[0]
            article_text += (article_class.cssselect("h1")[0]).text_content()

            ex_classes = doc.find_class('article_text')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p[:-1]:
                            article_text += "\n" + r.text_content()

            elif len(doc.find_class('lead')) != 0:
                ex_classes = doc.find_class('lead')
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p[:-1]:
                            article_text += "\n" + r.text_content()

            else:
                ex_classes = doc.find_class('title')
                par = ex_classes[0]
                article_text += par.text_content()

                ex_classes = doc.find_class('multimedia_main_content_text clearfix')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        all_p = par.findall("p")
                        if all_p:
                            for r in all_p[:]:
                                article_text += "\n" + r.text_content()
        except Exception as e:
            message = self.logger.make_message_link("AifuaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = AifuaParser(logger)
    # success, article = my_parser.parse('http://www.aif.ua/incidents/v_kieve_taksist_umer_za_rulem_avto_s_passazhirami')
    success, article = my_parser.parse('https://aif.ua/society/v_krymu_pochti_140_tysyach_chelovek_imeyut_biometricheskie_pasporta_ukrainy')
    # success, article = my_parser.parse(# 'http://www.aif.ua/vybory/rabinovich_my_provedem_uspeshnye_peregovory_o_snizhenii_cen_na_gaz') success,
    # article = my_parser.parse(
    # 'http://www.aif.ua/culture/festival_krasok_holi_2019_kak_v_indii_krasivo_vstrechayut_vesnu') success,
    # article = my_parser.parse('https://aif.ua/auto/pravitelstvo_gotovit_novuyu_formulu_rastamozhki_evroblyah')
    print(article)
