from gather.db import DbManager
from datetime import timedelta, date
from miscellanea.logging import FakeTestLogger
from ml.text import TextProcessor
import time


class ReportProcessor:

    def __init__(self, db_manager, text_processor):
        self.db_manager = db_manager
        pass

    # Создает перечисление дат с заданной начальной по конечную.
    def date_range(self, start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)

    # Возвращает словарь дат с количеством вхождения слова в статьи
    def get_word_in_texts_by_in_period(self, word, start_date, finish_date_include):
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

    # Возвращает словарь дат с количеством одновременного вхождения всех слов в статью
    def get_words_in_texts_by_in_period(self, words, start_date, finish_date_include):
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
    config_file = "e:\\Projects\\spiderstat\\config.json"
    logger = FakeTestLogger.FakeTestLogger()
    db_client = DbManager.DbManager(config_file, logger)
    processor = ReportProcessor(db_client, TextProcessor)

    begin = time.time()

    results = processor.get_word_in_texts_by_date('путин', date(2019, 3, 22), date(2019, 3, 22))

    end = time.time()
    diff = end - begin
    print("interval is: " + str(diff)+"\n")
    print(results[list(results)[0]])
