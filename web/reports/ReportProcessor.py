from gather.db import DbManager
from datetime import timedelta, date
from miscellanea.logging import FakeTestLogger
from ml.text import TextProcessor
import time
import mysql.connector
import os.path
from pathlib import Path
from miscellanea import ConfigManager
from dateutil.parser import parse
from datetime import datetime


class ReportProcessor:

    def __init__(self, db_connection):
        # self.db_cursor = db_cursor
        self.db_connection = db_connection
        # Хранит имена отчётов
        self.reports_name = []
        self.reports_name.append('war_test_report')

    # War test report

    def init_war_test_report(self):
        """
        Create new test report about using word 'war'
        """

        report_name = "war_test_report"
        cursor = self.db_connection.cursor()

        query = "SELECT MIN(pub_date) FROM publications"
        cursor.execute(query)
        min_date = parse(str(cursor.fetchone()[0])).date()

        query = "SELECT MAX(pub_date) FROM publications"
        cursor.execute(query)
        max_date = parse(str(cursor.fetchone()[0])).date()

        # check if report with this name exists already
        # if exists then delete
        query = "SELECT * FROM reports WHERE name = %s"
        cursor.execute(query, (report_name, ))
        rows = cursor.fetchall()
        if len(rows) != 0:
            query = "DELETE FROM reports WHERE name = %s"
            cursor.execute(query, (report_name, ))
            self.db_connection.commit()

        # insert report template
        query = "INSERT INTO reports (name, description, columns, x_title, y_title, body) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (report_name, 'test_report', "{'X':'number', 'Count':'number'}", 'Date', 'Count', ''))
        self.db_connection.commit()

        # select data from db and crate report
        report_dict = {}
        for date in self.date_range(min_date, max_date):
            war_counter = 0
            query = "SELECT full_article FROM publications WHERE %s<pub_date AND pub_date<%s"
            cursor.execute(query, (date, date + timedelta(1)))
            for row in cursor:
                article = row[0].lower()
                if "войн" in article:
                    war_counter += 1
            report_dict[str(date)] = war_counter

        result_string = ','.join([f"[{str(item)}, {str(report_dict[item])}]" for item in report_dict])

        # insert report in db
        query = "UPDATE reports SET body = %s WHERE name = %s"
        cursor.execute(query, (result_string, report_name))
        self.db_connection.commit()

    def create_war_test_report_for_one_day(self, report_date):
        """
        Дополняет отчет в БД статистикой за дату, переданную в параметре.
        """
        # Проверяем, есть ли такой отчет в БД. Если нет, то выходим.
        report_name = "war_test_report"
        cursor = self.db_connection.cursor()

        query = "SELECT * FROM reports WHERE name=%s LIMIT 1"
        cursor.execute(query, (report_name, ))
        rows = cursor.fetchall()
        if len(rows) == 0:
            return

        # Скачиваем отчет из БД.
        report_body = ""
        for row in rows:
            report_body = row[6]

        # Разбираем его на даты.
        splited_string = report_body.split("],[")
        splited_list = [item.replace("[", "").replace("]", "") for item in splited_string]
        splited_dict = {datetime.strptime(item.split(",")[0], "%Y-%m-%d").date(): item.split(",")[1] for item in splited_list}

        # Считаем статистику за данный день.
        war_counter = 0
        query = "SELECT full_article FROM publications WHERE pub_date = %s"
        cursor.execute(query, (report_date, ))
        for row in cursor:
            article = row[0].lower()
            if "войн" in article:
                war_counter += 1

        # Вносим изменения в локальное хранилище разбора.
        splited_dict[report_date] = war_counter

        # Сохраняем в БД.
        result_string = ','.join([f"[{str(item)}, {str(splited_dict[item])}]" for item in splited_dict])

        # insert report in db
        query = "UPDATE reports SET body = %s WHERE name = %s"
        cursor.execute(query, (result_string, report_name))
        self.db_connection.commit()

    # War test report

    def date_range(self, start_date, end_date):
        """
        Создает перечисление дат с заданной начальной по конечную.
        :param start_date:
        :param end_date:
        :return:
        """
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)

    def get_word_in_texts_by_in_period(self, word, start_date, finish_date_include):
        """Возвращает словарь дат с количеством вхождения слова в статьи"""
        result_dict = {}

        for single_date in self.date_range(start_date, finish_date_include):
            count = 0
            articles = self.db_manager.get_list_articles_by_date(single_date)
            for article in articles:
                article = text_processor.clean(article)
                if word in article:
                    count = count + 1

            result_dict[single_date] = count

        return result_dict

    def get_words_in_texts_by_in_period(self, words, start_date, finish_date_include):
        """
        Возвращает словарь дат с количеством одновременного вхождения всех слов в статью
        """
        result_dict = {}

        for single_date in self.date_range(start_date, finish_date_include):
            count = 0
            articles = self.db_manager.get_list_articles_by_date(single_date)
            for article in articles:
                article_word_count = 0
                article = text_processor.clean(article)
                for word in words:
                    if word in article:
                        article_word_count = article_word_count + 1
                if article_word_count == len(words):
                    count = count + 1

            result_dict[single_date] = count

        return result_dict

    def parse_json(self, json_body):
        pass

    def create_json(self, data):
        pass


if __name__ == "__main__":
    text_processor = TextProcessor.TextProcessor()
    main_dir = Path(__file__).parents[2]
    config_file = os.path.join(main_dir, "config.json")

    logger = FakeTestLogger.FakeTestLogger()

    configManager = ConfigManager.ConfigManager()
    configManager.read_config(config_file)

    user_name = configManager.db_username
    password = configManager.db_password
    host = configManager.db_host
    db_name = configManager.db_name

    connection = mysql.connector.connect(user=user_name, password=password, host=host, database=db_name)

    # db_client = DbManager(configManager, logger)
    processor = ReportProcessor(connection)

    test_name = "war"

    if test_name is "путин":
        begin = time.time()
        results = processor.get_word_in_texts_by_date('путин', date(2019, 3, 22), date(2019, 3, 22))

        end = time.time()
        diff = end - begin
        print("interval is: " + str(diff) + "\n")
        print(results[list(results)[0]])
    elif test_name is "war":
        # processor.init_war_test_report()
        processor.create_war_test_report_for_one_day(date(2019, 11, 1))
