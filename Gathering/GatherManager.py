from parsing.Russia import BbcParser, IzParser, LentaParser, LifeParser, MailParser, NewsruParser, PravdaParser, \
    RbcParser, RgParser, NsnParser, PolitexpertParser, RegnumruParser, RentvParser, RtParser, UraParser, ZnakParser
from parsing.Azerbaijan import AzsputniknewsParser, BrazParser, EchoazParser, KavkazuzelParser, MinvalazParser, \
    MisraParser, MusavatcomParser, NewsdayazParser, NewsmilliazParser, NovostiazParser, PrezidentazParser, \
    RegnumruazParser, ReportazParser, StatgovazParser, TrendazParser, VestikavkazaParser
from db import DbManager
from Gathering import RssClient
import time
from datetime import datetime
from miscellanea import Logger


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

    def add_russian_agencies(self, rss_clients, logger):
        rbc_parser = RbcParser.RbcParser(logger)
        rbc_rss_client = RssClient.RssClient(db_manager, 'www.rbc.ru', '0001.01.01 01:01:01', rbc_parser, 1, logger)
        rss_clients.append(rbc_rss_client)

        lenta_parser = LentaParser.LentaParser(logger)
        lenta_rss_client = RssClient.RssClient(db_manager, 'lenta.ru', '0001.01.01 01:01:01', lenta_parser, 1, logger)
        rss_clients.append(lenta_rss_client)

        life_parser = LifeParser.LifeParser(logger)
        life_rss_client = RssClient.RssClient(db_manager, 'life.ru', '0001.01.01 01:01:01', life_parser, 1, logger)
        rss_clients.append(life_rss_client)

        mail_parser = MailParser.MailParser(logger)
        mail_rss_client = RssClient.RssClient(db_manager, 'news.mail.ru', '0001.01.01 01:01:01',
                                              mail_parser, 1, logger)
        rss_clients.append(mail_rss_client)

        newsru_parser = NewsruParser.NewsruParser(logger)
        newsru_rss_client = RssClient.RssClient(db_manager, 'newsru.com', '0001.01.01 01:01:01',
                                                newsru_parser, 1, logger)
        rss_clients.append(newsru_rss_client)

        bbc_parser = BbcParser.BbcParser(logger)
        bbc_rss_client = RssClient.RssClient(db_manager, 'www.bbc.com/russian', '0001.01.01 01:01:01',
                                             bbc_parser, 1, logger)
        rss_clients.append(bbc_rss_client)

        rg_parser = RgParser.RgParser(logger)
        rg_rss_client = RssClient.RssClient(db_manager, 'rg.ru', '0001.01.01 01:01:01', rg_parser, 1, logger)
        rss_clients.append(rg_rss_client)

        iz_parser = IzParser.IzParser(logger)
        iz_rss_client = RssClient.RssClient(db_manager, 'iz.ru', '0001.01.01 01:01:01', iz_parser, 15, logger)
        rss_clients.append(iz_rss_client)

        pravda_parser = PravdaParser.PravdaParser(logger)
        pravda_rss_client = RssClient.RssClient(db_manager, 'pravda.ru', '0001.01.01 01:01:01',
                                                pravda_parser, 1, logger)
        rss_clients.append(pravda_rss_client)

        nsn_parser = NsnParser.NsnParser(logger)
        nsn_rss_client = RssClient.RssClient(db_manager, 'nsn.fm', '0001.01.01 01:01:01', nsn_parser, 1, logger)
        rss_clients.append(nsn_rss_client)

        polit_expert_parser = PolitexpertParser.PolitexpertParser(logger)
        polit_expert_rss_client = RssClient.RssClient(db_manager, 'politexpert.net', '0001.01.01 01:01:01',
                                                      polit_expert_parser, 1, logger)
        rss_clients.append(polit_expert_rss_client)

        regnumru_parser = RegnumruParser.RegnumruParser(logger)
        regnumru_rss_client = RssClient.RssClient(db_manager, 'regnum.ru', '0001.01.01 01:01:01',
                                                  regnumru_parser, 1, logger)
        rss_clients.append(regnumru_rss_client)

        rentv_parser = RentvParser.RentvParser(logger)
        rentv_rss_client = RssClient.RssClient(db_manager, 'ren.tv', '0001.01.01 01:01:01', rentv_parser, 1, logger)
        rss_clients.append(rentv_rss_client)

        rt_parser = RtParser.RtParser(logger)
        rt_rss_client = RssClient.RssClient(db_manager, 'russian.rt.com', '0001.01.01 01:01:01', rt_parser, 1, logger)
        rss_clients.append(rt_rss_client)

        ura_parser = UraParser.UraParser(logger)
        ura_rss_client = RssClient.RssClient(db_manager, 'ura.news', '0001.01.01 01:01:01', ura_parser, 1, logger)
        rss_clients.append(ura_rss_client)

        znak_parser = ZnakParser.ZnakParser(logger)
        znak_rss_client = RssClient.RssClient(db_manager, 'www.znak.com', '0001.01.01 01:01:01', znak_parser, 1, logger)
        rss_clients.append(znak_rss_client)

    def add_azerbaijani_agencies(self, rss_clients, logger):

        # https://az.sputniknews.ru/export/rss2/archive/index.xml
        azsputniknews_parser = AzsputniknewsParser.AzsputniknewsParser(logger)
        azsputniknews_rss_client = RssClient.RssClient(db_manager, 'az.sputniknews.ru', '0001.01.01 01:01:01',
                                                       azsputniknews_parser, 1, logger)
        rss_clients.append(azsputniknews_rss_client)

        # http://br.az/rss.php?sec_id
        braz_parser = BrazParser.BrazParser(logger)
        braz_rss_client = RssClient.RssClient(db_manager, 'br.az', '0001.01.01 01:01:01', braz_parser, 1, logger)
        rss_clients.append(braz_rss_client)

        # http://ru.echo.az/?feed=rss2
        echoaz_parser = EchoazParser.EchoazParser(logger)
        echoaz_rss_client = RssClient.RssClient(db_manager, 'ru.echo.az', '0001.01.01 01:01:01',
                                                echoaz_parser, 1, logger)
        rss_clients.append(echoaz_rss_client)

        # https://www.kavkaz-uzel.eu/articles.rss
        kavkazuzel_parser = KavkazuzelParser.KavkazuzelParser(logger)
        kavkazuzel_rss_client = RssClient.RssClient(db_manager, 'www.kavkaz-uzel.eu', '0001.01.01 01:01:01',
                                                    kavkazuzel_parser, 1, logger)
        rss_clients.append(kavkazuzel_rss_client)

        # https://minval.az/feed
        minvalaz_parser = MinvalazParser.MinvalazParser(logger)
        minvalaz_rss_client = RssClient.RssClient(db_manager, 'minval.az', '0001.01.01 01:01:01',
                                                  minvalaz_parser, 1, logger)
        rss_clients.append(minvalaz_rss_client)

        # http://misra.ru/feed/
        misra_parser = MisraParser.MisraParser(logger)
        misra_rss_client = RssClient.RssClient(db_manager, 'misra.ru', '0001.01.01 01:01:01',
                                               misra_parser, 1, logger)
        rss_clients.append(misra_rss_client)

        # http://musavat.com/rss.xml
        musavatcom_parser = MusavatcomParser.MusavatcomParser(logger)
        musavatcom_rss_client = RssClient.RssClient(db_manager, 'musavat.com', '0001.01.01 01:01:01',
                                                    musavatcom_parser, 1, logger)
        rss_clients.append(musavatcom_rss_client)

        # http://news.day.az/rss/all.rss
        newsdayaz_parser = NewsdayazParser.NewsdayazParser(logger)
        newsdayaz_rss_client = RssClient.RssClient(db_manager, 'news.day.az', '0001.01.01 01:01:01',
                                                   newsdayaz_parser, 1, logger)
        rss_clients.append(newsdayaz_rss_client)

        # https://news.milli.az/rss/
        newsmilliaz_parser = NewsmilliazParser.NewsmilliazParser(logger)
        newsmilliaz_rss_client = RssClient.RssClient(db_manager, 'news.milli.az', '0001.01.01 01:01:01',
                                                     newsmilliaz_parser, 1, logger)
        rss_clients.append(newsmilliaz_rss_client)

        # https://novosti.az/rss/all.rss
        novostiaz_parser = NovostiazParser.NovostiazParser(logger)
        novostiaz_rss_client = RssClient.RssClient(db_manager, 'novosti.az', '0001.01.01 01:01:01',
                                                   novostiaz_parser, 1, logger)
        rss_clients.append(novostiaz_rss_client)

        # https://ru.president.az/articles.rss
        prezident_parser = PrezidentazParser.PrezidentazParser(logger)
        prezidentaz_rss_client = RssClient.RssClient(db_manager, 'ru.president.az', '0001.01.01 01:01:01',
                                                     prezident_parser, 1, logger)
        rss_clients.append(prezidentaz_rss_client)

        # https://regnum.ru/rss/foreign/caucasia/azerbaijan
        regnumruaz_parser = RegnumruazParser.RegnumruazParser(logger)
        regnumruaz_rss_client = RssClient.RssClient(db_manager, 'regnum.ru/rss/foreign/caucasia/azerbaijan', '0001.01.01 01:01:01',
                                                    regnumruaz_parser, 1, logger)
        rss_clients.append(regnumruaz_rss_client)

        # https://report.az/rss/
        reportaz_parser = ReportazParser.ReportazParser(logger)
        reportaz_rss_client = RssClient.RssClient(db_manager, 'report.az', '0001.01.01 01:01:01',
                                                  reportaz_parser, 1, logger)
        rss_clients.append(reportaz_rss_client)

        # https://www.stat.gov.az/rss/az
        statgovaz_parser = StatgovazParser.StatgovazParser(logger)
        statgovaz_rss_client = RssClient.RssClient(db_manager, 'www.stat.gov.az', '0001.01.01 01:01:01',
                                                   statgovaz_parser, 1, logger)
        rss_clients.append(statgovaz_rss_client)

        # https://www.trend.az/feeds/index.rss
        trendaz_parser = TrendazParser.TrendazParser(logger)
        trendaz_rss_client = RssClient.RssClient(db_manager, 'www.trend.az', '0001.01.01 01:01:01',
                                                 trendaz_parser, 1, logger)
        rss_clients.append(trendaz_rss_client)

        # http://www.vestikavkaza.ru/newrss.php
        vestikavkaza_parser = VestikavkazaParser.VestikavkazaParser(logger)
        vestikavkaza_rss_client = RssClient.RssClient(db_manager, 'www.vestikavkaza.ru', '0001.01.01 01:01:01',
                                                      vestikavkaza_parser, 1, logger)
        rss_clients.append(vestikavkaza_rss_client)


if __name__ == "__main__":
    # TODO Вытаскивать учетные данные из конфига
    logger = Logger.Logger()
    db_manager = DbManager.DbManager('root', '', '127.0.0.1', 'spyder_stat', logger)
    rss_clients = []

    gather_manager = GatherManager(rss_clients, db_manager, 30 * 60)
    gather_manager.add_russian_agencies(rss_clients, logger)

    try:
        gather_manager.gather()
    except Exception as e:
            message = logger.make_message("Error in GatherManager", e, "")
            logger.write_message(message)
