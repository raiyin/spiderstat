import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class UraParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            e = doc.find_class('publication-title')[0]
            article_text += e.text_content()

            ex_classes = doc.find_class('item-text js-mediator-article')
            if len(ex_classes) != 0:
                for par in ex_classes[:-1]:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in UraParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = UraParser()
    # success, article = my_parser.parse('https://ura.news/news/1052369253')
    success, article = my_parser.parse('https://ura.news/news/1052369293')
    print(article)
