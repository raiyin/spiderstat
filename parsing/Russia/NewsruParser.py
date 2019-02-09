import sys
import urllib.request
from lxml.html import fromstring


class NewsruParser:

    def parse(self, url):
        try:
            article_text = ""
            content = urllib.request.urlopen(url).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)

            # Главный абзац новости
            ex_classes = doc.find_class('article-title')
            if len(ex_classes)!=0:
                e = ex_classes.pop()
                article_text += e.text_content().strip()

                # Текст новости
                e = doc.find_class('article-text').pop()
                r = e.findall("p")
                for par in r:
                    text = par.text_content().strip()
                    if text:
                        article_text += "\n" + text
            else:
                return 0, ""

        except Exception as e:
            print("Unexpected error in NewsruParser:", sys.exc_info()[0])
            print("error message is: " + str(e))
            print("url is: " + url)
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    my_parser = NewsruParser()
    success, article = my_parser.parse('https://www.newsru.com/world/18oct2018/volkerussnctns.html')
    print(article)
