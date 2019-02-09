import sys
import urllib.request
from lxml.html import fromstring


class RbcParser:

    def parse(self, url):
        try:
            article_text = ""
            content = urllib.request.urlopen(url).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)

            # Заголовок
            ex_classes = doc.find_class('article__header__title')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                article_text += e.text_content()

                # Текст новости
                e = doc.find_class('article__text').pop()
                r = e.findall("p")
                for par in r:
                    article_text += "\n" + par.text_content()
            else:
                return 0, ""

        except Exception as e:
            print("Unexpected error in RbcParser:", sys.exc_info()[0])
            print("error message is: " + str(e))
            print("url is: " + url)
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = RbcParser()
    success, article = my_parser.parse('https://www.rbc.ru/rbcfreenews/5bc8acd19a7947257ed65f69')
    print(article)
