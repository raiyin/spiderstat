from miscellanea.logging import FakeTestLogger
from miscellanea import ConfigManager
from reporting import ReportShell
from pathlib import Path
import mysql.connector
import datetime
import os.path
import json
import re


class NewsCount:

    def __init__(self, config_manager):
        self.user_name = config_manager.db_username
        self.password = config_manager.db_password
        self.host = config_manager.db_host
        self.db_name = config_manager.db_name

        self.connection = mysql.connector.connect(user=self.user_name, password=self.password,
                                                  host=self.host, database=self.db_name)
        self.cursor = self.connection.cursor(buffered=True)

        self.name = "news_count_by_day"
        self.description = "Показывает статистику количества новостей по суткам"
        self.columns = '{"Дата":"date", "Количество":"number"}'
        self.x_column_name = "Дата"
        self.y_column_name = "Количество"

    def create_report(self):
        """
        Создает пустую строку в таблице БД для отчета 'Количества новостей за сутки'.
        """

        try:
            delete_query = 'DELETE FROM reports WHERE name = %s'
            self.cursor.execute(delete_query, (self.name,))
            self.connection.commit()

            insert_query = "INSERT INTO reports (name, description, columns, x_title, y_title, body) VALUES (%s, %s, " \
                           "%s, %s, %s, %s) "

            self.cursor.execute(insert_query,
                                (self.name, self.description, self.columns, self.x_column_name, self.y_column_name, ""))
            self.connection.commit()
        except Exception as e:
            print(e)

    def first_completion(self):
        """
        Осуществляет первое заполнение отчета о количествах новостей по дням.
        """
        initial_query = 'SELECT DATE(pub_date), COUNT(*)  FROM publications GROUP BY DATE(pub_date)'
        self.cursor.execute(initial_query)

        report_string = ""

        try:
            for (report) in self.cursor:
                report_string += ("[" + str(report[0]) + ", " + str(report[1]) + "], ")

            if len(report_string) > 2:
                report_string = report_string[:-2]

            initial_query = "UPDATE reports SET body = %s WHERE name = %s"
            self.cursor.execute(initial_query, (report_string, self.name))
            self.connection.commit()
        except Exception as e:
            print(e)

        return report_string

    def day_reports_update(self, date):
        """
        Добавлет в отчет в БД данные за один день, переданный в параметре
        """
        try:
            # Получем уже имеющиеся данные в отчете в таблице.
            query = "SELECT body FROM  reports WHERE name = %s"
            self.cursor.execute(query, (self.name,))
            report_string = self.cursor.fetchone()[0]

            # Парсим их в массив и словарь
            report_array = report_string.split('], ')
            report_dict = {}
            for day_report in report_array:
                tmp = day_report.replace('[', '').replace(']', '')
                report_dict[datetime.datetime.strptime(tmp[0:tmp.find(',')], "%Y-%m-%d").date()] = tmp[tmp.find(',')+2:]

            # Обновляем их данными, посчитаными из БД, и сортируем массив по датам
            query = 'SELECT DATE(pub_date), COUNT(*)  FROM publications WHERE %s<pub_date AND pub_date<%s GROUP BY ' \
                    'DATE(pub_date)'
            self.cursor.execute(query, (str(date), str(date + datetime.timedelta(days=2))))

            # Добавляем данные о дате, переданной в качестве параметра.
            data = self.cursor.fetchone()
            report_dict[date] = data[1]
            report_string = ""

            # Создаем стоку тела отчета.
            for day_report in sorted(report_dict.keys()):
                report_string += ("[" + str(day_report) + ", " + str(report_dict[day_report]) + "], ")

            if len(report_string) > 2:
                report_string = report_string[:-2]

            # Обновляем строку в БД
            initial_query = "UPDATE reports SET body = %s WHERE name = %s"
            self.cursor.execute(initial_query, (report_string, self.name))
            self.connection.commit()

        except Exception as e:
            print(e)

    def get_report_ui(self):
        """
        Create report shell and fill it with data to draw report.
        :return:
        Filled report shell.
        """

        report_shell = ReportShell.ReportShell()

        query = "SELECT * FROM  reports WHERE name = %s"
        self.cursor.execute(query, (self.name,))
        query = self.cursor.fetchone()

        report_shell.id = query[0]
        report_shell.name = query[1]
        report_shell.description = query[2]
        report_shell.columns = json.loads(query[3])
        report_shell.x_title = query[4]
        report_shell.y_title = query[5]
        report_shell.data = query[6]

        # Костыль для верного отображения дат в js страницы.
        # Переделать так, чтобы информация бралась из столбца "columns".
        my_str = re.sub(r'(\d{4}?)-(\d{2}?)-(\d{2}?)', r'new Date(\1, \2, \3)', report_shell.data)
        report_shell.data = my_str

        return report_shell


if __name__ == "__main__":
    main_dir = Path(__file__).parents[1]
    config_file = os.path.join(main_dir, "config.json")
    logger = FakeTestLogger.FakeTestLogger()

    configManager = ConfigManager.ConfigManager()
    configManager.read_config(config_file)

    news_count_report = NewsCount(configManager)
    # news_count_report.day_reports_update(datetime.date(2019, 12, 4))
    # news_count_report.create_report()
    # news_count_report.first_completion()
    report_shell = news_count_report.get_report_ui()
    print(report_shell)
