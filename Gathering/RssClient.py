import feedparser
from db import DbManager
# for test purpose
from parsing.Russia import IzParser
import sys
import time


class RssClient:

    def __init__(self, db_manager, source_id, link, last_check_date, parser, timeout):
        self.db_manager = db_manager
        self.source_id = source_id
        self.link = link
        self.last_check_date = last_check_date
        self.parser = parser
        self.timeout = timeout

    def update_publications(self):
        try:
            publications = feedparser.parse(self.link)
        except Exception as e:
            print("Unexpected error in RssClient:", sys.exc_info()[0])
            print("error message is: " + str(e))
            print("url is: " + self.link)
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
                        print("\n==================================================")
                        print("Unexpected error in RssClient:", sys.exc_info()[0])
                        print("error message is: " + str(e))
                        print("url is: " + pub.link)
                        print("****************************************************\n")
                else:
                    print("error while page parsing, page is " + pub.link)


if __name__ == "__main__":
    local_db_manager = DbManager.DbManager('root', '', '127.0.0.1', 'spyder_stat')

    my_parser = IzParser.IzParser()
    rssClient = RssClient(local_db_manager, 1, 'https://iz.ru/xml/rss/all.xml', '0001.01.01 01:01:01', my_parser, 5)

    rssClient.update_publications()
