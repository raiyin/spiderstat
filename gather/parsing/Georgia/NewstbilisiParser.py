import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from miscellanea.logging import FakeTestLogger
from text.StringCleaner import StringCleaner


class NewstbilisiParser:

    def __init__(self, app_loger):
        self.logger = app_loger

    def parse(self, url):
        try:

            headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                       # "Accept-Encoding": "gzip, deflate, br",
                       "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                       "Cache-Control": "max-age=0",
                       "Connection": "keep-alive",
                       "Cookie": "last_visit=1553096672809::1553107472809; PHPSESSID=54c37b1e5bc384287cfd83e3ef10b3df",
                       "DNT": "1",
                       "Host": "newstbilisi.info",
                       "TE": "Trailers",
                       "Upgrade-Insecure-Requests": "1",
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"}
            # request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
            #                                               "(KHTML, like Gecko) Chrome/" + str(randint(40, 70)) +
            #                                               ".0.2227.0 Safari/537.36"})
            request = Request(url, headers=headers)
            # content = urllib.request.urlopen(request).read().decode('utf-8')
            content = urllib.request.urlopen(request).read().strip().decode(errors='replace')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            # ex_classes = doc.find_class('name post-title entry-title')
            # par = ex_classes[0]
            # article_text += par.text_content()

            ex_classes = doc.find_class('entry-content clearfix')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n" + r.text_content()
        except Exception as e:
            message = self.logger.make_message("NewstbilisiParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = NewstbilisiParser(logger)
    success, article = my_parser.parse('https://newstbilisi.info/145579-a-potom-my-tancevali-otkroet-krupnejshij'
                                       '-kinofestival-norvegii-novosti-gruziya.html')
    # success, article = my_parser.parse('https://newstbilisi.info/145531-pervyj-inklyuzivnyj-plyazh-otkrylsya-v-batumi'
    #                                   '-novosti-gruziya.html')
    print(article)
