from random import randint
from fake_useragent import UserAgent


class HttpHeadersFactory:

    def __init__(self):
        pass

    def get_user_agent_header(self):
        headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
                                 "(KHTML, like Gecko) Chrome/" + str(randint(40, 70)) +
                                 ".0.2227.0 Safari/537.36"}
        return headers

    def get_cookie_header(self, url):
        pass
