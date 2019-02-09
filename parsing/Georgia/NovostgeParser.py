import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class NovostgeParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('entry-title')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            ex_classes = doc.find_class('entry-content')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in NovostgeParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = NovostgeParser()
    #success, article = my_parser.parse('http://novost.ge/2019/02/05/%d0%b2-%d0%bf%d0%be%d1%80%d1%82%d1%83-%d0%bf%d0'
    #                                   '%be%d1%82%d0%b8-%d0%b0%d0%bc%d0%b5%d1%80%d0%b8%d0%ba%d0%b0%d0%bd%d1%81%d0%ba'
    #                                   '%d0%b0%d1%8f-%d0%ba%d0%be%d1%80%d0%bf%d0%be%d1%80%d0%b0%d1%86%d0%b8%d1%8f/')
    success, article = my_parser.parse('http://novost.ge/2019/02/05/%d0%b3%d1%80%d1%83%d0%b7%d0%b8%d1%8f-%d0%bf%d0%be'
                                       '%d0%bf%d0%b0%d0%bb%d0%b0-%d0%b2-%d1%80%d0%b5%d0%b9%d1%82%d0%b8%d0%bd%d0%b3'
                                       '-%d0%ba%d1%80%d1%83%d0%bf%d0%bd%d0%b5%d0%b9%d1%88%d0%b8%d1%85-%d1%81%d1%82/')
    print(article)
