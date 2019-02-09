import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class IpressgeParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('post-title')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            ex_classes = doc.find_class('single-post-excerpt post-excerpt-bc')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()

            ex_classes = doc.find_class('entry-content clearfix single-post-content')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in IpressgeParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = IpressgeParser()
    success, article = my_parser.parse('https://ipress.ge/new/elene-khoshtaria-otsneba-im-absurdamde-mivida-rom-lamis'
                                       '-beseliats-natsmodzraoba-gakhda/')
    #success, article = my_parser.parse('https://ipress.ge/new/khoshtaria-chinchaladze-gakhda-thqveni-ghmerthi'
    #                                   '-ivanishvilma-ki-murusidze-lambaqze-dasva-da-samudamod-dagvado/')
    print(article)
