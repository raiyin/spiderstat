from random import randint


class RequestHeaderGenerator:
    def __init__(self):
        pass

    @staticmethod
    def get_headers():
        headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                 "(KHTML, like Gecko) Chrome/" + str(randint(70, 73)) +
                                 ".0.2227.0 Safari/537.36"}
        return headers
