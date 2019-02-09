import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class NbnewscomuaParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('entry-header')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("h1")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()

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
            print("Error in NbnewscomuaParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = NbnewscomuaParser()
    #success, article = my_parser.parse('https://nbnews.com.ua/za-rubezhom/2019/02/03/severnaia-koreia-vsled-za'
    #                                   '-rossiei-podderjala-madyro/')
    success, article = my_parser.parse('https://nbnews.com.ua/politika/2019/02/03/vybory-prezidenta-segodnia-yje-7'
                                       '-chelovek-prinesli-dokymenty-v-cik/')
    print(article)
