import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class InfonineParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)
            article_text = ""

            ex_classes = doc.find_class('article_title')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            ex_classes = doc.find_class('article-content')
            par = ex_classes[0]
            article_text += "\n"+par.text_content()

            #ex_classes = doc.find_class('article-content')
            #if len(ex_classes) != 0:
            #    for par in ex_classes:
            #        all_p = par.findall("p")
            #        if all_p:
            #            for r in all_p:
            #                article_text += "\n"+r.text_content()
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in InfonineParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = InfonineParser()
    #success, article = my_parser.parse('http://www.info9.ge/politika/203857-uzenaes-sasamarthloshi-dimitri'
    #                                   '-gvritishvilis-kandidaturas-chemi-mkhardatcera-ar-eqneba--thamar-chugoshvili'
    #                                   '.html?lang=ka-GE&utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A'
    #                                   '+info9+%28Info9.Ge%29&utm_content=FeedBurner')
    success, article = my_parser.parse('http://www.info9.ge/uckhoethi/203853-donald-tuski-adamianebisthvis-vinc'
                                       '-britaneths-samoqmedo-gegmis-gareshe-evrokavshiridan-gasvlisken-moutsodebda'
                                       '-jojokhethshi-calke-adgilia-gamoyofili.html?lang=ka-GE&utm_source=feedburner'
                                       '&utm_medium=feed&utm_campaign=Feed%3A+info9+%28Info9.Ge%29&utm_content'
                                       '=FeedBurner')
    print(article)
