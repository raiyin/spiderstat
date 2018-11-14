import sys
import urllib.request
from urllib.request import Request
from lxml.html import fromstring


class LifeParser:

    content = ""

    def parse(self, url):
        try:
            article_text = ""

            request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                                          "(KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})

            content = urllib.request.urlopen(request).read()

            doc = fromstring(content)
            doc.make_links_absolute(url)

            # Заголовок, если он есть.
            ex_classes = doc.find_class('post-page-header')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                r = e.findall("h1")
                for par in r:
                    # Красивая проверка, что строка не пустая
                    if par.text_content():
                        article_text += "\n" + par.text_content()

                # Текст новости
                e = doc.find_class('content-note').pop()
                r = e.findall("p")
                for par in r:
                    # Красивая проверка, что строка не пустая.
                    if par.text_content():
                        article_text += "\n" + par.text_content()

        except Exception as e:
            try:
                # Возможно, другой тип статьи
                doc = fromstring(content)  # .decode('utf-8'))
                doc.make_links_absolute(url)
                ex_classes = doc.find_class('longreads-subtitle')
                if len(ex_classes) != 0:
                    e = ex_classes.pop()
                    article_text += e.text_content()

                # Текст новости
                ex_classes = doc.find_class('content-note')
                if len(ex_classes) != 0:
                    e = ex_classes.pop()
                    r = e.findall("p")
                    for par in r:
                        # Красивая проверка, что строка не пустая.
                        if par.text_content():
                            article_text += "\n" + par.text_content()

                return 1, article_text
            except Exception as e:
                print("=================================================")
                type_, value_, traceback_ = sys.exc_info()
                print("Error in LifeParser")
                print("Error type is:", type_)
                print("Error value is ", value_)
                print("Error traceback is:", traceback_)
                print("error message is: " + str(e))

                print("url is: " + url)
                print("*************************************************")
                return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = LifeParser()
    # success, article = my_parser.parse('https://life.ru/1165470')
    success, article = my_parser.parse('https://life.ru/t/%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8/1166353/ekspiert_rasskazal_kak_vozmozhnoie_naznachieniie_noiiert_skazhietsia_na_otnoshieniiakh_s_rf')
    print(article)
