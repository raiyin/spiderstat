import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class KpuaParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/" + str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('content-img')
            e = ex_classes.pop()
            r = e.findall("img")[0]
            article_text += str(r.xpath('//img/@alt')[1])

            ex_classes = doc.find_class('content')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                r = e.findall("p")
                for par in r:
                    article_text += par.text_content()
            else:
                return 0, ""
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in KpuaParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = KpuaParser()
    success, article = my_parser.parse('https://kp.ua/culture/629471-pevytsa-yulyia-savycheva-poteriala-pervoho-rebenka')
    #success, article = my_parser.parse('https://kp.ua/politics/629469-poroshenko-soobschyl-chto-podpysal-vazhnyi'
    #                                   '-zakon-o-perekhode-k-pravoslavnoi-tserkvy-ukrayny')
    print(article)
