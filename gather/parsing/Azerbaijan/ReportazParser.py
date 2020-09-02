import urllib.request
from urllib.request import Request
from lxml.html import fromstring
from random import randint
from miscellanea.logging import FakeTestLogger
from ml.text.StringCleaner import StringCleaner
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os
from pathlib import Path
from miscellanea import ConfigManager


class ReportazParser:

    def __init__(self, app_logger, config_manager):
        self.logger = app_logger
        self.config_manager = config_manager

    def parse(self, url):
        try:
            executable_path = self.config_manager.gecko_driver_path
            driver = webdriver.Firefox(executable_path=executable_path, service_log_path=os.devnull)
            driver.get(url)
            elem = driver.find_element_by_class_name("news-title")
            article_text = elem.text + "\n"
            elem = driver.find_element_by_class_name("editor-body")
            article_text += elem.text
            driver.close()
        except Exception as e:
            message = self.logger.make_message_link("ReportazParser", e, url)
            self.logger.write_message(message)
            return 0, ""
        article_text = StringCleaner.clean(article_text)
        return 1, article_text

    #def parse(self, url):
    #    try:
    #        down_article = Article(url)
    #        down_article.download()
    #        down_article.parse()
    #        article_text = down_article.text
    #    except Exception as e:
    #        message = self.logger.make_message_link("ReportazParser", e, url)
    #        self.logger.write_message(message)
    #        return 0, ""
    #    article_text = StringCleaner.clean(article_text)
    #    return 1, article_text


if __name__ == "__main__":
    main_dir = Path(__file__).parents[3]
    config_file = os.path.join(main_dir, "config.json")
    configManager = ConfigManager.ConfigManager()
    configManager.read_config(config_file)

    logger = FakeTestLogger.FakeTestLogger()
    my_parser = ReportazParser(logger, configManager)

    # success, article = my_parser.parse('https://report.az/diger-olkeler/seudiyye-erebistaninda-da-koronavirusa-ilk-yoluxma-askarlandi/')
    # success, article = my_parser.parse('https://report.az/diger-olkeler/abs-da-immiqrasiya-muveqqeti-dayandirilacaq/')
    success, article = my_parser.parse('https://report.az/az/xarici-siyaset/ceyhun-bayramov-kuveytin-azerbaycandaki-sefiri-ile-gorusub/')
    # success, article = my_parser.parse('https://report.az/ru/ikt/exxonmobil-mozhet-nachat-ispol-zovat-kvantovye-komp'
    #                                    '-yutery-ibm/')
    print(article)
