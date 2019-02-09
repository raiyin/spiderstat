import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class ZnakParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)

            ex_classes = doc.find_class('flex x3 article-wrapper')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                r = e.findall("article/p")
                article_text = ""
                for par in r:
                    article_text += "\n" + par.text_content()
            else:
                return 0, ""
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in ZnakParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = ZnakParser()
    # success, article = my_parser.parse('https://www.znak.com/2019-01-25/reuters_naemniki_iz_chvk_vagner_priehali_v_venesuelu_chtoby_ohranyat_maduro')
    success, article = my_parser.parse('https://www.znak.com/2019-01-25/reyting_doveriya_putinu_pobil_istoricheskiy_minimum')
    print(article)