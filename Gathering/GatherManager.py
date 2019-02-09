from parsing.Russia import BbcParser, IzParser, LentaParser, LifeParser, MailParser, NewsruParser, PravdaParser, \
    RbcParser, RgParser
from miscellanea import MailSender
from db import DbManager
from Gathering import RssClient
import time
from datetime import datetime
import sys


class GatherManager:
    def __init__(self, rss_clients, db_manager, pause_interval):
        self.rss_clients = rss_clients
        self.pause = pause_interval
        self.db_manager = db_manager

    def gather(self):
        while True:
            for rss_client in self.rss_clients:
                try:
                    print("load " + rss_client.link)
                    rss_client.update_publications()
                    self.db_manager.update_last_check_date(rss_client.source_id, str(datetime.now()))
                    self.db_manager.check_and_reconnect()
                except:
                    self.db_manager.check_and_reconnect()
                    continue
            print("Circle done...")
            print(datetime.now())
            time.sleep(self.pause)


if __name__ == "__main__":
    db_manager = DbManager.DbManager('root', '', '127.0.0.1', 'spyder_stat')
    rss_clients = []

    rbc_parser = RbcParser.RbcParser()
    rbc_source_rss = db_manager.get_rss_url_by_link('www.rbc.ru')
    rbc_rss_client = RssClient.RssClient(db_manager, 1, rbc_source_rss, '0001.01.01 01:01:01', rbc_parser, 1)

    lenta_parser = LentaParser.LentaParser()
    lenta_source_rss = db_manager.get_rss_url_by_link('lenta.ru')
    lenta_rss_client = RssClient.RssClient(db_manager, 2, lenta_source_rss, '0001.01.01 01:01:01', lenta_parser, 1)

    life_parser = LifeParser.LifeParser()
    life_source_rss = db_manager.get_rss_url_by_link('life.ru')
    life_rss_client = RssClient.RssClient(db_manager, 3, life_source_rss, '0001.01.01 01:01:01', life_parser, 1)

    mail_parser = MailParser.MailParser()
    mail_source_rss = db_manager.get_rss_url_by_link('news.mail.ru')
    mail_rss_client = RssClient.RssClient(db_manager, 4, mail_source_rss, '0001.01.01 01:01:01', mail_parser, 1)

    newsru_parser = NewsruParser.NewsruParser()
    newsru_source_rss = db_manager.get_rss_url_by_link('newsru.com')
    newsru_rss_client = RssClient.RssClient(db_manager, 5, newsru_source_rss, '0001.01.01 01:01:01', newsru_parser, 1)

    bbc_parser = BbcParser.BbcParser()
    bbc_source_rss = db_manager.get_rss_url_by_link('www.bbc.com/russian')
    bbc_rss_client = RssClient.RssClient(db_manager, 6, bbc_source_rss, '0001.01.01 01:01:01', bbc_parser, 1)

    rg_parser = RgParser.RgParser()
    rg_source_rss = db_manager.get_rss_url_by_link('rg.ru')
    rg_rss_client = RssClient.RssClient(db_manager, 7, rg_source_rss, '0001.01.01 01:01:01', rg_parser, 1)

    iz_parser = IzParser.IzParser()
    iz_source_rss = db_manager.get_rss_url_by_link('iz.ru')
    iz_rss_client = RssClient.RssClient(db_manager, 8, iz_source_rss, '0001.01.01 01:01:01', iz_parser, 15)

    pravda_parser = PravdaParser.PravdaParser()
    pravda_source_rss = db_manager.get_rss_url_by_link('pravda.ru')
    pravda_rss_client = RssClient.RssClient(db_manager, 9, pravda_source_rss, '0001.01.01 01:01:01', pravda_parser, 1)

    rss_clients.append(rbc_rss_client)
    rss_clients.append(lenta_rss_client)
    rss_clients.append(life_rss_client)
    rss_clients.append(mail_rss_client)
    rss_clients.append(newsru_rss_client)
    rss_clients.append(bbc_rss_client)
    rss_clients.append(rg_rss_client)
    rss_clients.append(iz_rss_client)
    rss_clients.append(pravda_rss_client)

    gather_manager = GatherManager(rss_clients, db_manager, 30 * 60)

    try:
        gather_manager.gather()
    except Exception as e:
        type_, value_, traceback_ = sys.exc_info()
        text = "Error type is:" + str(type_) + "\n"
        text += "Error value is " + str(value_) + "\n"
        text += "Error traceback is:" + str(traceback_) + "\n"
        text += "error message is: " + str(e)

        sender = MailSender.MailSender()
        sender.send_mail("login@ya.ru", "password", "Отчет об ошибке", text)

# !!! https://www.znak.com/rss
# !!! https://politexpert.net/feed
# !!! http://ren.tv/export/feed.xml
# !!! https://russian.rt.com/rss
# !!! http://nsn.fm/rss/
# !!! https://ura.news/rss
