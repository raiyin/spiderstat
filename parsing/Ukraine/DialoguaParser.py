import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class DialoguaParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/" + str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('news-news clearfix')[0]
            tag = ex_classes.findall('h1')[0]
            article_text += tag.text_content()

            par = doc.find_class('news-text')[0]
            article_text += '\n'+par.text_content()

            ex_classes = doc.find_class('news-text')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n" + r.text_content()
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in DialoguaParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = DialoguaParser()
    success, article = my_parser.parse('https://www.dialog.ua/ukraine/170684_1548847344')
    #success, article = my_parser.parse('https://www.dialog.ua/war/170677_1548841514')
    print(article)