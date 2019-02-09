### Доработать
import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class ZnajParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            e = doc.find_class('col-8')[0]
            all_hone = e.findall('article/header/h1')[0]
            article_text += all_hone.text_content()

            ex_classes = doc.find_class('article-body')
            finded_class = ex_classes[0]
            all_p = finded_class.findall("p")
            for p in all_p:
                article_text += "\n" + p.text_content()
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in ZnajParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = ZnajParser()
    #success, article = my_parser.parse('https://znaj.ua/society/206327-privatbank-potrapiv-u-zhahliviy-skandal-z'
    #                                   '-vigadanimi-borgami-takih-shahrajiv-shche-poshukati-treba')
    #success, article = my_parser.parse('https://znaj.ua/society/206325-vchiteliv-zmusyat-zdavati-zno-de-i-koli')
    success, article = my_parser.parse('https://znaj.ua/society/206340-fiziognomist-poyasnila-shcho-prihovuye-zelenskiy-uvaga-na-ochi-ta-nis')
    print(article)
