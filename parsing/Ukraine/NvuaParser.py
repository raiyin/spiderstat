import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class NvuaParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/" + str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('article__content__head__text')[0]
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
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in NvuaParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = NvuaParser()
    # success, article = my_parser.parse('https://nv.ua/world/countries/v-gaage-proizoshel-moshchnyy-vzryv-50003384
    # .html')
    # success, article = my_parser.parse(
    # 'https://nv.ua/ukraine/events/boeviki-odin-raz-obstrelyali-ukrainskie-pozicii-oos-50003383.html')
    success, article = my_parser.parse('https://nv.ua/ukraine/events/sezd-po-vydvizheniju-timoshenko-deputat'
                                       '-transhender-i-zapreshchennaja-literatura-luchshee-za-nedelju-po-versii'
                                       '-hlavreda-nvua--2517354.html')
    print(article)
