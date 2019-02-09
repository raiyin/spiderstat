import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class RentvParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            e = doc.find_class('news clearfix')
            for par in e:
                # Красивая проверка на непустоту списка
                all_p = par.findall("h1")
                if all_p:
                    r = all_p.pop()
                    article_text += "\n" + r.text_content()

            article_text += "\n"
            ex_classes = doc.find_class('field-item even')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    article_text += "\n" + par.text_content()
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in RentvParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = RentvParser()
    # success, article = my_parser.parse('http://ren.tv/node/383290')
    success, article = my_parser.parse('http://ren.tv/node/383293')
    print(article)