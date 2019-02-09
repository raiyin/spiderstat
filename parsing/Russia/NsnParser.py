import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class NsnParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            e = doc.find_class('b-editor-article__header__title').pop()
            article_text += e.text_content()

            #e = doc.find_class('article__summary').pop()
            #article_text += "\n" + e.text_content()

            ex_classes = doc.find_class('b-editor-article__body')
            if len(ex_classes) != 0:
                for par in ex_classes[:-1]:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += r.text_content()
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in NsnParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = NsnParser()
    #  success, article = my_parser.parse('http://nsn.fm/hots/inflyaciya-v-venesuele-v-2019-godu-prevysit-10000000.html')
    success, article = my_parser.parse('http://nsn.fm/hots/lukashenko-podderzhivaet-maduro.html')
    print(article)
