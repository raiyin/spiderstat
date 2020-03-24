import mysql.connector
from datetime import datetime, date
from miscellanea.logging import FakeTestLogger
from collections import namedtuple
import os.path
from pathlib import Path
from miscellanea import ConfigManager


class FakeDbManager:

    def __init__(self):
        pass
        #self.user_name = config_manager.db_username
        #self.password = config_manager.db_password
        #self.host = config_manager.db_host
        #self.db_name = config_manager.db_name

        #self.connection = mysql.connector.connect(user=self.user_name, password=self.password,
        #                                          host=self.host, database=self.db_name)
        #self.cursor = self.connection.cursor(buffered=True)
        #self.logger = my_logger

    def get_rss_url_by_link(self, link):
        return link

    def get_source_id_by_link(self, link):
        return link

    def check_publication_in_db(self, pub_id, source_id):
        return False
