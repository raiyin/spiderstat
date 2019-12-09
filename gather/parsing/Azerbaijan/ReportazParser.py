import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from text.StringCleaner import StringCleaner
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os


class ReportazParser:

    def __init__(self, app_logger):
        self.logger = app_logger

    def parse(self, url):
        try:
            executable_path = r'e:\Projects\spiderstat\bin\geckodriver.exe'
            driver = webdriver.Firefox(executable_path=executable_path, service_log_path=os.devnull)
            driver.get(url)
            elem = driver.find_element_by_class_name("short-news-header")
            article_text = elem.text + "\n"
            elem = driver.find_element_by_class_name("post-text")
            article_text += elem.text
            driver.close()

            # request = Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
            #                                              "(KHTML, like Gecko) Chrome/" + str(randint(40, 70)) +
            #                                              ".0.2227.0 Safari/537.36"})

            # content = urllib.request.urlopen(request).read().decode('utf-8')
            # doc = fromstring(content)
            # doc.make_links_absolute(url)
            # article_text = ""

            # ex_classes = doc.find_class('short-news-header')
            # par = ex_classes[0]
            # article_text += par.text_content()
            # ex_classes = doc.find_class('post-text')
            # if len(ex_classes) != 0:
            #     for par in ex_classes:
            #         all_p = par.findall("p")
            #         if all_p:
            #             for r in all_p:
            #                 article_text += "\n" + r.text_content()
        except Exception as e:
            message = self.logger.make_message_link("ReportazParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger()
    my_parser = ReportazParser(logger)
    success, article = my_parser.parse(
        'https://report.az/diger-olkeler/i-raqda-abs-herbcileri-novbeti-hucuma-meruz-qaliblar/')
    # success, article = my_parser.parse('https://report.az/ru/ikt/exxonmobil-mozhet-nachat-ispol-zovat-kvantovye-komp'
    #                                    '-yutery-ibm/')
    print(article)
