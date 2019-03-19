import smtplib
from email.message import EmailMessage


class MailSender:

    def __init__(self, login, password, server, port):
        self.login = login
        self.password = password
        self.server = server
        self.port = port

        # create server
        self.smtp_server = smtplib.SMTP_SSL(self.server, self.port)
        self.smtp_server.login(self.login, self.password)

    def close(self):
        self.smtp_server.quit()

    def send_mail(self, subject, text):

        # setup the parameters of the message
        msg = EmailMessage()
        msg['From'] = self.login
        msg['To'] = self.login
        msg['Subject'] = subject
        msg['Importance'] = "High"
        msg.set_content(text)

        try:
            status = self.smtp_server.noop()[0]
        except:
            status = -1

        if status == 250:
            try:
                self.smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())
            except Exception as e:
                print("Failed to send message. Text is: " + text)
                print("\nSending exception is:" + str(e))
        else:
            self.smtp_server.login(self.login, self.password)
            # send the message via the server.
            try:
                self.smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())
            except Exception as e:
                print("Failed to send message. Text is: " + text)
                print("\nSending exception is:" + str(e))
