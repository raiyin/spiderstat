import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class VistiproParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('field field--name-title field--type-string')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            ex_classes = doc.find_class('clearfix text-formatted field')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    article_text += par.text_content()
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in VistiproParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = VistiproParser()
    success, article = my_parser.parse('http://visti.pro/uk/ekonomika-ta-finansi/za-minuliy-rik-borgi-po-komunalci-virosli-na-23-mlrd-grn')
    #success, article = my_parser.parse('http://visti.pro/uk/podii/politvyaznyu-pavlu-gribu-viklikali-shvidku-pid-chas-sudovogo-zasidannya')
    print(article)
