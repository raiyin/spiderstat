import json


class ConfigManager:

    def __init__(self):

        # mysql
        self.db_username = ""
        self.db_password = ""
        self.db_host = ""
        self.db_name = ""

        # smtp
        self.smtp_login = ""
        self.smtp_password = ""
        self.smtp_server = ""
        self.smtp_port = ""

        # misc
        self.restore_work_timeout = 30 * 60
        self.backup_enabled = True
        self.backup_timeout = 0
        self.backup_source_dir = ""
        self.backup_dest_dir = ""
        self.gecko_driver_path = ""

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
            self.restore_work_timeout = misc["restore_work_timeout"]
            self.backup_timeout = misc["backup_timeout"]
            self.backup_enabled = misc["backup_enable"]
            self.backup_source_dir = misc["backup_source_dir"]
            self.backup_dest_dir = misc["backup_dest_dir"]
            self.gecko_driver_path = misc["gecko_driver_path"]

    def write_config(self):
        pass
