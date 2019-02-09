import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class UkranewsParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('article_title')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            ex_classes = doc.find_class('anotation')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            ex_classes = doc.find_class('article_content')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in UkranewsParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = UkranewsParser()
    #success, article = my_parser.parse('https://ukranews.com/interview/2112-artur-mkhitaryan-pervyi-shag-sdelan'
    #                                   '-skhema-doivshaya-stroitelei-mnogo-let-razrushena')
    success, article = my_parser.parse('https://ukranews.com/publication/2594-novaya-fishka-prezidenta-subsidii-s'
                                       '-marta-nachnut-vydavat-zhivymi-dengami')
    print(article)
