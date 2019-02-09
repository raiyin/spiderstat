import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class AllnewsParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('text')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("h1")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()

            ex_classes = doc.get_element_by_id('insertAdArea')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in AllnewsParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = AllnewsParser()
    #success, article = my_parser.parse('https://www.allnews.ge/sazogadoeba/163633-%E1%83%AB%E1%83%9A%E1%83%98%E1%83'
    #                                   '%94%E1%83%A0%E1%83%98-%E1%83%A5%E1%83%90%E1%83%A0%E1%83%98-%E1%83%93%E1%83%90'
    #                                   '-21-%E1%83%92%E1%83%A0%E1%83%90%E1%83%93%E1%83%A3%E1%83%A1%E1%83%98-%E1%83%A1'
    #                                   '%E1%83%98%E1%83%97%E1%83%91%E1%83%9D-%E1%83%A0%E1%83%9D%E1%83%92%E1%83%9D%E1'
    #                                   '%83%A0-%E1%83%90%E1%83%9B%E1%83%98%E1%83%9C%E1%83%93%E1%83%A1-%E1%83%9E%E1%83'
    #                                   '%A0%E1%83%9D%E1%83%92%E1%83%9C%E1%83%9D%E1%83%96%E1%83%98%E1%83%A0%E1%83%94'
    #                                   '%E1%83%91%E1%83%94%E1%83%9C-%E1%83%A3%E1%83%90%E1%83%AE%E1%83%9A%E1%83%9D%E1'
    #                                   '%83%94%E1%83%A1-%E1%83%93%E1%83%A6%E1%83%94%E1%83%94%E1%83%91%E1%83%A8%E1%83'
    #                                   '%98.html')
    success, article = my_parser.parse('https://www.allnews.ge/%E1%83%92%E1%83%90%E1%83%9C%E1%83%90%E1%83%97%E1%83%9A'
                                       '%E1%83%94%E1%83%91%E1%83%90/163638-%E1%83%9B%E1%83%90%E1%83%A1%E1%83%AC%E1%83'
                                       '%90%E1%83%95%E1%83%9A%E1%83%94%E1%83%91%E1%83%94%E1%83%9A%E1%83%97%E1%83%90'
                                       '-%E1%83%A1%E1%83%94%E1%83%A0%E1%83%A2%E1%83%98%E1%83%A4%E1%83%98%E1%83%AA%E1'
                                       '%83%98%E1%83%A0%E1%83%94%E1%83%91%E1%83%98%E1%83%A1-%E1%83%90%E1%83%AE%E1%83'
                                       '%90%E1%83%9A%E1%83%98-%E1%83%9B%E1%83%9D%E1%83%93%E1%83%94%E1%83%9A%E1%83%98'
                                       '-%E1%83%93%E1%83%90-%E1%83%A1%E1%83%90%E1%83%AE%E1%83%94%E1%83%9A%E1%83%A4%E1'
                                       '%83%90%E1%83%A1%E1%83%9D-%E1%83%9E%E1%83%9D%E1%83%9A%E1%83%98%E1%83%A2%E1%83'
                                       '%98%E1%83%99%E1%83%90-%E1%83%A8%E1%83%94%E1%83%9B%E1%83%A3%E1%83%A8%E1%83%90'
                                       '%E1%83%95%E1%83%93%E1%83%94%E1%83%91%E1%83%90.html')
    print(article)
