import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from text.StringCleaner import StringCleaner


class NvuaParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/" + str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            need_classes = doc.find_class('article__content__head__text')

            if len(need_classes) != 0:
                ex_classes = need_classes[0]
                tag = ex_classes.findall('h1')[0]
                article_text += tag.text_content()

                ex_classes = doc.find_class('subtitle')[0]
                article_text += '\n' + ex_classes.text_content()

                ex_classes = doc.find_class('content_wrapper')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        all_p = par.findall("p")
                        if all_p:
                            for r in all_p:
                                article_text += "\n" + r.text_content()
            elif len(doc.find_class('article__content__head')) != 0:
                need_classes = doc.find_class('article__content__head')
                ex_classes = need_classes[0]
                tag = ex_classes.findall('h1')[0]
                article_text += tag.text_content()

                ex_classes = doc.find_class('subtitle')[0]
                article_text += '\n' + ex_classes.text_content()

                ex_classes = doc.find_class('content_wrapper')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        all_p = par.findall("p")
                        if all_p:
                            for r in all_p:
                                article_text += "\n" + r.text_content()
            elif len(doc.find_class('head_content')) != 0:
                need_classes = doc.find_class('head_content')
                ex_classes = need_classes[0]
                tag = ex_classes.findall('h1')[0]
                article_text += tag.text_content()

                # ex_classes = doc.find_class('subtitle')[0]
                # article_text += '\n' + ex_classes.text_content()

                ex_classes = doc.find_class('article_body')
                if len(ex_classes) != 0:
                    for par in ex_classes:
                        all_p = par.findall("p")
                        if all_p:
                            for r in all_p:
                                article_text += "\n" + r.text_content()

        except Exception as e:
            message = self.logger.make_message("NvuaParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = NvuaParser(logger)
    # success, article = my_parser.parse('https://nv.ua/world/countries/v-gaage-proizoshel-moshchnyy-vzryv-50003384
    # .html') success, article = my_parser.parse(
    # 'https://nv.ua/ukraine/events/boeviki-odin-raz-obstrelyali-ukrainskie-pozicii-oos-50003383.html') success,
    # article = my_parser.parse('https://style.nv.ua/blogs/kak-pridumat-neobychnoe-rezyume-i-poluchit-rabotu-50012495
    # .html')
    success, article = my_parser.parse(
        'https://techno.nv.ua/gadgets/samsung-galaxy-s10-plus-vs-huawei-p30-pro-50014025.html')
    print(article)
