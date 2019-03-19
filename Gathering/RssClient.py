import feedparser
from db import DbManager
# for test purpose
from parsing.Russia import IzParser
import time
from miscellanea import FakeTestLogger


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
        try:
            publications = feedparser.parse(self.link)
        except Exception as e:
            message = self.logger.make_message("RssClient parse error", e, self.link)
            self.logger.write_message(message)
            return
        for pub in publications.entries:
            # Проверяем, если данная публикация в базе
            if self.db_manager.check_publication_in_db(pub.id, self.source_id):
                continue
            else:
                # Сохраняем публикацию в базу
                success, article = self.parser.parse(pub.link)
                time.sleep(self.timeout)
                if success:
                    try:
                        self.db_manager.save_publication(pub.title, pub.link,
                                                         (pub.description if hasattr(pub, 'description') else ""),
                                                         article, pub.published_parsed, pub.id, self.source_id)
                    except Exception as e:
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
