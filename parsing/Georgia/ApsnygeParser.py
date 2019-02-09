import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class ApsnygeParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('article')
            par = ex_classes[0]
            article_text += par.text_content()

            ex_classes = doc.find_class('txt-item-news')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    article_text += '\n'+par.text_content()
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in ApsnygeParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = ApsnygeParser()
    #success, article = my_parser.parse('https://www.apsny.ge/2019/pol/1549427079.php')
    success, article = my_parser.parse('https://www.apsny.ge/2019/eco/1549427740.php')
    print(article)
