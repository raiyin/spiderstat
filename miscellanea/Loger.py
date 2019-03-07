from miscellanea import MailSender


class Loger:

    def __init__(self, login, password, server, port):
        self.mail_server = MailSender.MailSender(login, password, server, port)

    def write_message(self, message):
        self.mail_server.send_mail("Отчет об ошибке", message)


if __name__ == "__main__":
    loger = Loger('raiyin@ya.ru', 'password', 'smtp.yandex.ru', 465)
    loger.write_message("testing loger")
