import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class SobitiyaParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('publicFull')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("h1/b")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()

            ex_classes = doc.find_class('text')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("index/p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in SobitiyaParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = SobitiyaParser()
    #success, article = my_parser.parse('http://www.sobytiya.info/news/u-beregov-kryma-gremeli-vystrely')
    success, article = my_parser.parse('http://www.sobytiya.info/news/propavshiy-bez-vesti-kapitan-krymskogo-sudna'
                                       '-mog-pokinut-ukrainu-advokat')
    print(article)
