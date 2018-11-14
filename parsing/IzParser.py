import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class IzParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)

            ex_classes = doc.find_class('text-article__inside')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                r = e.findall("div/div/p")
                article_text = ""
                for par in r:
                    article_text += "\n" + par.text_content()
            else:
                return 0, ""
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in IzParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = IzParser()
    # success, article = my_parser.parse('https://iz.ru/805117/georgii-oltarzhevskii/vzryv-pokrovov-kto-podorval-linkor-novorossiisk')
    success, article = my_parser.parse('https://iz.ru/808585/2018-11-05/dva-zdaniia-obrushilis-v-tcentre-marselia')
    print(article)
