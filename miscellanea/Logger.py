from miscellanea import MailSender
from miscellanea import FakeTestLogger
import json
import sys
import traceback


class Logger:

    def __init__(self, config_manager):
        login = config_manager.login
        password = config_manager.password
        server = config_manager.server
        port = config_manager.port

        self.mail_server = MailSender.MailSender(login, password, server, port)

    def write_message(self, message):
        self.mail_server.send_mail("Отчет об ошибке", message)

    def make_message(self, parser_name, exception, url):
        message = "=================================================\n"

        type_, value_, traceback_ = sys.exc_info()
        exc_info = sys.exc_info()

        message += "Error in " + parser_name + "\n"
        message += "Error type:" + str(type_) + "\n"
        message += "Error value: " + str(value_) + "\n"
        message += "Error traceback: " + str(traceback_) + "\n"
        message += "Error traceback: " + str(traceback.print_exception(*exc_info)) + "\n"
        message += "error message: " + str(exception) + "\n"
        message += "url: " + url + "\n"
        message += "*************************************************" + "\n"
        return message


if __name__ == "__main__":
    logger = Logger("e:\\Projects\\spiderstat\\config.json")
    logger.write_message("testing logger")
