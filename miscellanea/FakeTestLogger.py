

class FakeTestLogger:

    def __init__(self):
        pass

    def write_message(self, message):
        print(str(message))

    def make_message(self, parser_name, exception, url):
        pass


if __name__ == "__main__":
    logger = FakeTestLogger()
    logger.write_message("testing logger")
