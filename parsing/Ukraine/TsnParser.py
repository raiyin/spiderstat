import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class TsnParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('p-name c-post-title u-uppercase js-si-title')[0]
            article_text += ex_classes.text_content()

            ex_classes = doc.find_class('p-summary c-post-lead')[0]
            #r = ex_classes.findall("p")[0]
            article_text += '\n' + ex_classes.text_content()

            ex_classes = doc.find_class('e-content')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n" + r.text_content()
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in TsnParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = TsnParser()
    #success, article = my_parser.parse('https://tsn.ua/svit/u-siriyi-naymanci-rf-ta-iranu-vlashtuvali-mizh-soboyu'
    #                                   '-perestrilku-zmi-1286781.html')
    success, article = my_parser.parse('https://tsn.ua/ukrayina/ukrayinskiy-universitet-nadav-patriarhu-varfolomiyu'
                                       '-zvannya-pochesnogo-doktora-1286775.html')
    print(article)