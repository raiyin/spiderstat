import smtplib
from email.message import EmailMessage


class MailSender:

    def send_mail(self, login, password, subject, text):

        # setup the parameters of the message
        msg = EmailMessage()
        msg['From'] = login
        msg['To'] = login
        msg['Subject'] = subject
        msg['Importance'] = "High"
        msg.set_content(text)

        # create server
        server = smtplib.SMTP_SSL("smtp.yandex.ru", 465)
        server.login(msg['From'], password)

        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())

        server.quit()


if __name__ == "__main__":
    sender = MailSender()
    sender.send_mail("login@ya.ru", "password", "Subject is Отчет об ошибке", "Text is The error has occured")
    print("sending ended")
