import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class KorrespondentParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('post-item__text')
            if len(ex_classes) != 0:
                    r = ex_classes[0].findall("h2")[0]
                    article_text += r.text_content()

            ex_classes = doc.find_class('post-item__text')[0]
            all_p = ex_classes.findall("p")
            for r in all_p[:-1]:
                article_text += r.text_content()

        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in KorrespondentParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = KorrespondentParser()
    success, article = my_parser.parse('https://korrespondent.net/world/4058023-lukashenko-lychno-zaveryl-maduro-v'
                                       '-podderzhke')
    # success, article = my_parser.parse('https://korrespondent.net/city/kharkov/4058033-v-kharkove-muzhchyna
    # -yznasyloval-devushku-provyzora-v-apteke')
    print(article)