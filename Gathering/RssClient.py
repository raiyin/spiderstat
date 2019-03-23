import feedparser
from db import DbManager
# for test purpose
from parsing.Russia import IzParser
import time
from miscellanea import FakeTestLogger
import datetime
from collections import namedtuple
from random import randint


class RssClient:

    def __init__(self, db_manager, link, last_check_date, parser, timeout, logger):

        self.db_manager = db_manager
        self.source_id = self.db_manager.get_source_id_by_link(link)
        self.link = db_manager.get_rss_url_by_link(link)
        self.last_check_date = last_check_date
        self.parser = parser
        self.timeout = timeout
        self.logger = logger


    def update_publications(self):
        """Проверяет наличие публикации в базе и, если ее нет, то сохраняет в БД."""
        try:
            browser_rev = str(randint(60, 66))
            publications = feedparser.parse(self.link,
                                            request_headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:"+browser_rev+".0) Gecko/20100101 Firefox/"+browser_rev+".0",
                                                             'Accept-Encoding': "gzip, deflate, br",
                                                             'Accept-Language': "en-US,en;q=0.8,en-US;q=0.5,en;q=0.3",
                                                             'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                                             'Connection': "keep-alive",
                                                             'Cookie': "4ad6446af5040292949818c55c0ceec4=q1m1613pr75jfdrc29pjvqctv7",
                                                             'DNT': "1",
                                                             'Upgrade-Insecure-Requests': "1"})
        except Exception as e:
            message = self.logger.make_message("RssClient parse error", e, self.link)
            self.logger.write_message(message)
            return
        for pub in publications.entries:
            # Проверяем, если данная публикация в базе
            if hasattr(pub, "id"):
                pub_id = pub.id
            else:
                pub_id = pub.link
            if self.db_manager.check_publication_in_db(pub_id, self.source_id):
                continue
            else:
                # Сохраняем публикацию в базу
                success, article = self.parser.parse(pub.link)
                time.sleep(self.timeout)
                if success:
                    try:
                        self.db_manager.save_publication(pub.title, pub.link,
                                                         (pub.description if hasattr(pub, 'description') else ""),
                                                         article, pub.published_parsed, pub_id, self.source_id)
                    except Exception as e:
                        # ошибка в дате.
                        if str(e.__class__) == "<class 'mysql.connector.errors.DataError'>":
                            now = datetime.datetime.now()
                            Published_parsed = namedtuple("published_parsed",
                                                          "tm_year tm_mon tm_mday tm_hour tm_min tm_sec")
                            published_parsed = Published_parsed(
                                tm_year=str(now.year),
                                tm_mon=str(now.month),
                                tm_mday=str(now.day),
                                tm_hour=str(now.hour),
                                tm_min=str(now.minute),
                                tm_sec=str(now.second))

                            self.db_manager.save_publication(pub.title, pub.link,
                                                             (pub.description if hasattr(pub, 'description') else ""),
                                                             article, published_parsed, pub_id, self.source_id)
                        else:
                            message = self.logger.make_message("RssClient parse error", e, self.link)
                            self.logger.write_message(message)
                            return
                else:
                    print("error while page parsing, page is " + pub.link)


if __name__ == "__main__":
    logger = FakeTestLogger.FakeTestLogger('', '', 'smtp.yandex.ru', 465)
    local_db_manager = DbManager.DbManager('root', '', '127.0.0.1', 'spyder_stat')

    my_parser = IzParser.IzParser()
    rssClient = RssClient(local_db_manager, 1, 'https://iz.ru/xml/rss/all.xml',
                          '0001.01.01 01:01:01', my_parser, 5, logger)

    rssClient.update_publications()
