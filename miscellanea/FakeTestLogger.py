

class FakeTestLogger:

    def __init__(self, login, password, server, port):
        pass

    def write_message(self, message):
        pass

    def make_message(self, parser_name, exception, url):
        pass


if __name__ == "__main__":
    logger = FakeTestLogger('raiyin@ya.ru', 'password', 'smtp.yandex.ru', 465)
    logger.write_message("testing logger")
