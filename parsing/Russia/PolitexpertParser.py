import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class PolitexpertParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)

            ex_classes = doc.find_class('js-mediator-article')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                r = e.findall("p")
                article_text = ""
                for par in r[:-1]:
                    article_text += "\n" + par.text_content()
            else:
                return 0, ""
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in PolitexpertParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = PolitexpertParser()
    success, article = my_parser.parse('https://politexpert.net/139050-venesuela-prodolzhit-prodavat-neft-ssha-maduro')
    # success, article = my_parser.parse('https://politexpert.net/139048-nad-alpami-turisticheskii-samolet-stolknulsya-s-vertoletom-est-pogibshie')
    print(article)
