from miscellanea import MailSender
from miscellanea import FakeTestLogger
import json
import sys


class Logger:

    def __init__(self, config_file):
        with open(config_file) as json_config_data:
            data = json.load(json_config_data)
            smtp = data["smtp"]
            login = smtp["login"]
            password = smtp["password"]
            server = smtp["server"]
            port = smtp["port"]

        self.mail_server = MailSender.MailSender(login, password, server, port)

    def write_message(self, message):
        self.mail_server.send_mail("Отчет об ошибке", message)

    def make_message(self, parser_name, exception, url):
        message = "=================================================\n"
        type_, value_, traceback_ = sys.exc_info()
        message += "Error in " + parser_name + "\n"
        message += "Error type:" + str(type_) + "\n"
        message += "Error value: " + str(value_) + "\n"
        message += "Error traceback: " + str(traceback_) + "\n"
        message += "error message: " + str(exception) + "\n"
        message += "url: " + url + "\n"
        message += "*************************************************" + "\n"
        return message


if __name__ == "__main__":
    logger = Logger("e:\\Projects\\spiderstat\\config.json")
    logger.write_message("testing logger")
