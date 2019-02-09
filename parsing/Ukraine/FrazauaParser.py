import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint


class FrazauaParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
            doc = fromstring(content)
            doc.make_links_absolute(url)

            ex_classes = doc.find_class('article__title article__title__big')
            par = ex_classes[0]
            article_text = par.text_content()

            ex_classes = doc.find_class('article__summary')
            if len(ex_classes) != 0:
                for par in ex_classes:
                    all_p = par.findall("div/p")
                    if all_p:
                        for r in all_p:
                            article_text += "\n"+r.text_content()
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in FrazauaParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = FrazauaParser()
    #success, article = my_parser.parse('https://fraza.ua/video/275776'
    #                                   '-v_set_popalo_video_grandioznogo_proryva_damby_v_brazilii')
    success, article = my_parser.parse('https://fraza.ua/news/275775-suprugi-belovy-podlo-obmanuli-nikolaevskogo'
                                       '-strelka-bagirjantsa-smi')
    print(article)
