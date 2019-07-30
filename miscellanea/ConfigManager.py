import json


class ConfigManager:

    def __init__(self):

        # mysql
        self.user_name = ""
        self.password = ""
        self.host = ""
        self.db_name = ""

        # smtp
        self.login = ""
        self.password = ""
        self.server = ""
        self.port = ""

        # misc
        self.timeout = 0

    def read_config(self, config_file):
        with open(config_file) as json_config_data:
            data = json.load(json_config_data)
            my_sql = data["mysql"]
            self.db_username = my_sql["user"]
            self.db_password = my_sql["passwd"]
            self.db_host = my_sql["host"]
            self.db_name = my_sql["db"]

            smtp = data["smtp"]
            self.smtp_login = smtp["login"]
            self.smtp_password = smtp["password"]
            self.smtp_server = smtp["server"]
            self.smtp_port = smtp["port"]

            misc = data["misc"]
            self.timeout = misc["timeout"]

    def write_config(self):
        pass
