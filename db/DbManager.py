import mysql.connector
from datetime import datetime, date
from miscellanea import FakeTestLogger
from collections import namedtuple
import mysql.connector


class DbManager:

    def __init__(self, config_manager, logger):
        self.user_name = config_manager.db_username
        self.password = config_manager.db_password
        self.host = config_manager.db_host
        self.db_name = config_manager.db_name

        self.connection = mysql.connector.connect(user=self.user_name, password=self.password,
                                                  host=self.host, database=self.db_name)
        self.cursor = self.connection.cursor(buffered=True)
        self.logger = logger

    def print_companies(self):
        query = "SELECT company_name FROM companies"
        self.cursor.execute(query)

        for (company_name) in self.cursor:
            print("{}".format(company_name))

    def get_companies_list(self):
        query = "SELECT company_name FROM companies"
        self.cursor.execute(query)
        companies = []

        for (company_name) in self.cursor:
            companies.append(company_name[0])

        return companies

    def check_and_reconnect(self):
        sq = "SELECT NOW()"
        try:
            self.cursor.execute(sq)
        except:
            self.connection = mysql.connector.connect(user=self.user_name,
                                                      password=self.password,
                                                      host=self.host,
                                                      database=self.db_name)
            self.cursor = self.connection.cursor(buffered=True)

    def get_rss_urls_list(self):
        query = "SELECT source_rss FROM info_sources"
        self.cursor.execute(query)
        urls = []

        for (rss_url) in self.cursor:
            urls.append(rss_url[0])

        return urls

    def get_rss_url_by_link(self, link):
        self.check_and_reconnect()
        query = "SELECT source_rss FROM info_sources WHERE link = %s"
        self.cursor.execute(query, (link,))
        return self.cursor.fetchone()[0]

    def get_source_id_by_link(self, link):
        self.check_and_reconnect()
        query = "SELECT source_id FROM info_sources WHERE link = %s"
        self.cursor.execute(query, (link,))
        return self.cursor.fetchone()[0]

    def update_last_check_date(self, source_id, date):
        self.check_and_reconnect()
        query = "UPDATE info_sources SET last_check_date = %s WHERE source_id = %s"
        self.cursor.execute(query, (date, str(source_id)))
        self.connection.commit()

    def check_publication_in_db(self, guid, source_id):
        try:
            self.check_and_reconnect()
            query = "SELECT COUNT(pub_id) FROM publications WHERE guid = %s AND info_source_id = %s"
            self.cursor.execute(query, (guid, str(source_id)))
        except Exception as e:
            message = self.logger.make_message("Unexpected error in check_publication_in_db. Query is: " +
                                               query + "\nsource_id is: " + str(source_id), e, "")
            self.logger.write_message(message)
            return 0, ""

        return self.cursor.fetchone()[0] > 0

    def save_publication(self, title, link, description, article, pub_date, guid, info_source_id):

        # There are errors in pub_date
        is_error_in_date = False

        if int(pub_date.tm_year) < 2000 or int(pub_date.tm_year) > 2100:
            is_error_in_date = True

        if int(pub_date.tm_mon) < 0 or int(pub_date.tm_mon) > 12:
            is_error_in_date = True

        if int(pub_date.tm_mday) < 0 or int(pub_date.tm_mday) > 31:
            is_error_in_date = True

        if is_error_in_date:
            now = datetime.datetime.now()
            Published_parsed = namedtuple("published_parsed",
                                          "tm_year tm_mon tm_mday tm_hour tm_min tm_sec")
            pub_date = Published_parsed(
                                tm_year=str(now.year),
                                tm_mon=str(now.month),
                                tm_mday=str(now.day),
                                tm_hour=str(now.hour),
                                tm_min=str(now.minute),
                                tm_sec=str(now.second))

        query = "INSERT INTO publications (info_source_id, title, link, description, full_article, pub_date, guid)" + \
                " VALUES (%s, %s, %s, %s, %s, %s, %s)"

        try:
            self.cursor.execute(query, (str(info_source_id),
                                        title,
                                        link,
                                        str(description),
                                        article,
                                        str(pub_date.tm_year) + "." + str(pub_date.tm_mon) + "." + str(
                                            pub_date.tm_mday) + " " +
                                        str(pub_date.tm_hour) + ":" + str(pub_date.tm_min) + ":" + str(pub_date.tm_sec),
                                        guid))
            self.connection.commit()
        except Exception as e:
            message = self.logger.make_message("Unexpected error in save_publication. Query is: " + query + "\n" +
                                               "title is: " + title + "\n" +
                                               "link is: " + link + "\n" +
                                               "description is: " + description + "\n" +
                                               "article is: " + article + "\n" +
                                               "info_source_id is: " + str(info_source_id), e, "")
            self.logger.write_message(message)

    def get_list_articles_by_date(self, current_date):
        query = "SELECT full_article FROM publications WHERE DATE(pub_date) = '" + current_date.strftime(
            "%Y-%m-%d") + "'"
        self.cursor.execute(query)
        articles = []

        for (article) in self.cursor:
            articles.append(article[0])

        return articles

    def get_articles_count(self):
        query = "SELECT COUNT(*) FROM publications"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]


if __name__ == "__main__":

    print(datetime.now().year)
    print(datetime.now().month)
    print(datetime.now().day)

    config_file = "e:\\Projects\\spiderstat\\config.json"
    logger = FakeTestLogger.FakeTestLogger()
    db_client = DbManager(config_file, logger)
    mode = 'get_articles_count'

    if mode == 'print_companies':
        db_client.print_companies()
    elif mode == 'get_companies_list':
        for company in db_client.get_companies_list():
            print(company)
    elif mode == 'get_rss_urls_list':
        for url in db_client.get_rss_urls_list():
            print(url)
    elif mode == 'update_last_check_date':
        # db_client.update_last_check_date(1, '2018-10-18 01:01:01')
        db_client.update_last_check_date(1, str(datetime.now()))
    elif mode == "check_publication_in_db":
        print(db_client.check_publication_in_db('https://iz.ru/805396/video/kannskie-lvy-v-moskve', 1))
    elif mode == 'get_rss_url_by_link':
        print(db_client.get_rss_url_by_link('www.rbc.ru'))
    elif mode == "get_articles":
        check_date = date(2019, 3, 23)
        articles = db_client.get_list_articles_by_date(check_date)
        print(len(articles))
    elif mode == "get_articles_count":
        count = db_client.get_articles_count()
        print(count)
