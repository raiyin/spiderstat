import sys
import urllib.request
from lxml.html import fromstring
from miscellanea import Loger


class BbcParser:

    def __init__(self, loger):
        self.loger = loger

    def parse(self, url):
        try:
            article_text = ""
            content = urllib.request.urlopen(url).read()
            doc = fromstring(content)
            doc.make_links_absolute(url)

            # Главный абзац новости
            ex_classes = doc.find_class('story-body__h1')
            if len(ex_classes) != 0:
                e = ex_classes.pop()
                article_text += e.text_content().strip()

                # Текст новости
                e = doc.find_class('story-body__inner').pop()
                r = e.findall("p")
                for par in r:
                    text = par.text_content().strip()
                    if text:
                        article_text += "\n" + text
            elif len(doc.find_class('vxp-media__headline')) != 0:
                ex_classes = doc.find_class('vxp-media__headline')
                e = ex_classes.pop()
                article_text += e.text_content().strip()

                # Текст новости
                e = doc.find_class('vxp-media__summary').pop()
                r = e.findall("p")
                for par in r:
                    text = par.text_content().strip()
                    if text:
                        article_text += "\n" + text
            else:
                return 0, ""

        except Exception as e:
            message = "Unexpected error in BbcParser: " + str(sys.exc_info()[0])
            message += "error message is: " + str(e)
            message += "url is: " + url
            self.loger.write_message(message)
            return 0, ""
        return 1, article_text


if __name__ == "__main__":
    loger = Loger.Loger('', '', '', 465)
    my_parser = BbcParser(loger)
    success, article = my_parser.parse('https://www.bbc.com/russian/features-46067230')
    # success, article = my_parser.parse('https://www.bbc.com/russian/av/media-45904959')

    print(article)
