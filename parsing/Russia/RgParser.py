import sys
import urllib.request
from lxml.html import fromstring


class RgParser:

    def parse(self, url):
        try:
            article_text = ""
            content = urllib.request.urlopen(url).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)

            # Главный абзац новости
            ex_classes = doc.find_class('b-material-wrapper__lead')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                article_text += e.text_content()

                # Текст новости
                e = doc.find_class('b-material-wrapper__text').pop()
                r = e.findall("p")
                for par in r:
                    article_text += "\n" + par.text_content()

            elif len(doc.find_class('b-material-head__title'))!=0:
                ex_classes = doc.find_class('b-material-head__title')
                e = ex_classes.pop()
                article_text += e.text_content()

                # Текст новости
                e = doc.find_class('b-material-wrapper__text').pop()
                r = e.findall("p")
                for par in r:
                    article_text += "\n" + par.text_content()
            else:
                return 0, ""
        except Exception as e:
            print("Unexpected error in RgParser:", sys.exc_info()[0])
            print("error message is: " + str(e))
            print("url is: " + url)
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = RgParser()
    # success, article = my_parser.parse('https://rg.ru/2018/10/18/cb-nameren-otmenit-bankovskoe-rabstvo.html')
    success, article = my_parser.parse(
        'https://rg.ru/2018/10/30/sotni-avtomobilej-maserati-sgoreli-pri-pozhare-v-italii.html')

    print(article)
