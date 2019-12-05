from db import DbManager
from miscellanea import FakeTestLogger
from datetime import datetime, date, time, timedelta
from miscellanea import ConfigManager
import os.path
from pathlib import Path


class QueryMaster:
    """Helps to make reports

    Longer class information....

    Attributes:
    """
    def __init__(self, dbManager):
        self.dbManager = dbManager

    def day_articles_count(self, date):
        query = "SELECT COUNT(*) FROM publications WHERE %s<pub_date AND pub_date<%s"
        return self.dbManager.query_executor(query, (date, date + timedelta(days=1)))


if __name__ == "__main__":
    main_dir = Path(__file__).parents[1]
    config_file = os.path.join(main_dir, "config.json")

    logger = FakeTestLogger.FakeTestLogger()

    configManager = ConfigManager.ConfigManager()
    configManager.read_config(config_file)

    db_client = DbManager.DbManager(configManager, logger)

    query_master = QueryMaster(db_client)
    result = query_master.day_articles_count(date(2018, 10, 25))
    print(result)
