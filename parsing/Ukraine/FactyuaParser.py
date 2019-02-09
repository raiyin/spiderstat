import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from bs4 import BeautifulSoup


class FactyuaParser:

    def parse(self, url):
        try:

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/"+str(randint(40, 70)) +
                                                          ".0.2227.0 Safari/537.36"})
            content = urllib.request.urlopen(request).read().decode('utf-8')
            soup = BeautifulSoup(content, 'html5lib')
            doc = fromstring(content)

            article_text = ""

            e = doc.find_class('zag3')[0]
            article_text += e.text_content()

            paragraphs = soup.find(id='article_content3').find_all()[:-2]
            for element in paragraphs:
                article_text += str(element.text)
        except Exception as e:
            print("=================================================")
            type_, value_, traceback_ = sys.exc_info()
            print("Error in FactyuaParser")
            print("Error type is:", type_)
            print("Error value is ", value_)
            print("Error traceback is:", traceback_)
            print("error message is: " + str(e))

            print("url is: " + url)
            print("*************************************************")
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = FactyuaParser()
    #success, article = my_parser.parse('https://fakty.ua/294365-bud-ty-proklyata-vesna---2014-v-krymu-na-stende-s-gazetami-razmestili-lyubopytnoe-obyavlenie')
    success, article = my_parser.parse('https://fakty.ua/294361-v-ukraine-vtroe-snizili-normy-potrebleniya-gaza-chto-budet-s-cenami-na-kommunalku')
    print(article)
