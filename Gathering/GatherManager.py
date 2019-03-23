from parsing.Russia import BbcParser, IzParser, LentaParser, LifeParser, MailParser, NewsruParser, PravdaParser, \
    RbcParser, RgParser, NsnParser, PolitexpertParser, RegnumruParser, RentvParser, RtParser, UraParser, ZnakParser
from parsing.Azerbaijan import AzsputniknewsParser, BrazParser, EchoazParser, KavkazuzelParser, MinvalazParser, \
    MisraParser, MusavatcomParser, NewsdayazParser, NewsmilliazParser, NovostiazParser, PrezidentazParser, \
    RegnumruazParser, ReportazParser, StatgovazParser, TrendazParser, VestikavkazaParser
from parsing.Georgia import AkhalitaobaParser, AllnewsParser, ApsnygeParser, BfmParser, CbwgeParser, \
    EuronewsgeParser, InfonineParser, IpressgeParser, JnewsParser, NewsgeParser, NewstbilisiParser, \
    NovostgeParser, ReportioriParser, SovanewsParser, SputnikgeorgiaParser, TabulaParser
from parsing.Ukraine import AifuaParser, CapitaluaParser, DaykyivuaParser, DialoguaParser, FactycomuaParser, \
    FactyuaParser, FinanceuaParser, ForuaParser, FrazauaParser, GazetaUaParser, GoloscomuaParser, GolosuaParser, \
    InterfaxcomuaParser, IpressuaParser, IzvestiakievuaParser, KontraktyParser, KorrespondentParser, KpuaParser, \
    KratkonewsParser, NbnewscomuaParser, NewsobozParser, NuainuaParser, NvuaParser, ObozrevatelParser, \
    OdessalifeParser, OneonetwoParser, PressorgParser, SobytiyaParser, TsnParser, UkranewsParser, UkrinformParser,\
    VestiuaParser, VestiukrParser, VistiproParser, VlastinetParser, ZahidParser, ZnajParser
from db import DbManager
from Gathering import RssClient
import time
from datetime import datetime
from miscellanea import Logger


class GatherManager:
    def __init__(self, rss_clients, db_manager, pause_interval, logger):
        self.rss_clients = rss_clients
        self.pause = pause_interval
        self.db_manager = db_manager
        self.logger = logger

    def gather(self):
        while True:
            for rss_client in self.rss_clients:
                try:
                    print("load " + rss_client.link)
                    rss_client.update_publications()
                    self.db_manager.update_last_check_date(rss_client.source_id, str(datetime.now()))
                    self.db_manager.check_and_reconnect()
                except Exception as e:
                    message = self.logger.make_message("Error in gather function", e, str(rss_client))
                    self.logger.write_message(message)
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

    def add_georgian_agencies(self, rss_clients, logger):

        # Error 400 bad request.
        # https://www.allnews.ge/?format=feed&type=rss
        # allnews_parser = AllnewsParser.AllnewsParser(logger)
        # allnews_rss_client = RssClient.RssClient(db_manager, 'www.allnews.ge', '0001.01.01 01:01:01',
        #                                          allnews_parser, 1, logger)
        # rss_clients.append(allnews_rss_client)

        # http://akhalitaoba.ge/feed/
        akhalitaoba_parser = AkhalitaobaParser.AkhalitaobaParser(logger)
        akhalitaoba_rss_client = RssClient.RssClient(db_manager, 'akhalitaoba.ge', '0001.01.01 01:01:01',
                                                     akhalitaoba_parser, 1, logger)
        rss_clients.append(akhalitaoba_rss_client)

        # https://apsny.ge/RSS.xml
        apsnyge_parser = ApsnygeParser.ApsnygeParser(logger)
        apsny_rss_client = RssClient.RssClient(db_manager, 'apsny.ge', '0001.01.01 01:01:01', apsnyge_parser, 1, logger)
        rss_clients.append(apsny_rss_client)

        # http://bfm.ge/feed/
        bfm_parser = BfmParser.BfmParser(logger)
        bfm_rss_client = RssClient.RssClient(db_manager, 'bfm.ge', '0001.01.01 01:01:01', bfm_parser, 1, logger)
        rss_clients.append(bfm_rss_client)

        # http://cbw.ge/feed/
        cbwge_parser = CbwgeParser.CbwgeParser(logger)
        cbwge_rss_client = RssClient.RssClient(db_manager, 'cbw.ge', '0001.01.01 01:01:01', cbwge_parser, 1, logger)
        rss_clients.append(cbwge_rss_client)

        # http://euronews.ge/feed/
        euronewsge_parser = EuronewsgeParser.EuronewsgeParser(logger)
        euronews_rss_client = RssClient.RssClient(db_manager, 'euronews.ge', '0001.01.01 01:01:01', euronewsge_parser,
                                                  1, logger)
        rss_clients.append(euronews_rss_client)

        # http://feeds.feedburner.com/info9?format=xml
        infonine_parser = InfonineParser.InfonineParser(logger)
        infonine_rss_client = RssClient.RssClient(db_manager, 'www.info9.ge', '0001.01.01 01:01:01', infonine_parser,
                                                  1, logger)
        rss_clients.append(infonine_rss_client)

        # https://ipress.ge/feed/rss/
        ipressge_parser = IpressgeParser.IpressgeParser(logger)
        ipressge_rss_client = RssClient.RssClient(db_manager, 'ipress.ge', '0001.01.01 01:01:01', ipressge_parser,
                                                  1, logger)
        rss_clients.append(ipressge_rss_client)

        # http://jnews.ge/?feed=rss2
        jnews_parser = JnewsParser.JnewsParser(logger)
        jnews_rss_client = RssClient.RssClient(db_manager, 'jnews.ge', '0001.01.01 01:01:01', jnews_parser, 1, logger)
        rss_clients.append(jnews_rss_client)

        # https://news.ge/feed/
        newsge_parser = NewsgeParser.NewsgeParser(logger)
        newsge_rss_client = RssClient.RssClient(db_manager, 'news.ge', '0001.01.01 01:01:01', newsge_parser, 1, logger)
        rss_clients.append(newsge_rss_client)

        # https://newstbilisi.info/feed/
        newstbilisi_parser = NewstbilisiParser.NewstbilisiParser(logger)
        newstbilisi_rss_client = RssClient.RssClient(db_manager, 'newstbilisi.info', '0001.01.01 01:01:01',
                                                     newstbilisi_parser, 1, logger)
        rss_clients.append(newstbilisi_rss_client)

        # http://novost.ge/feed/
        novostge_parser = NovostgeParser.NovostgeParser(logger)
        novostge_rss_client = RssClient.RssClient(db_manager, 'novost.ge', '0001.01.01 01:01:01', novostge_parser,
                                                  1, logger)
        rss_clients.append(novostge_rss_client)

        # http://reportiori.ge/rss.php
        reportiori_parser = ReportioriParser.ReportioriParser(logger)
        reportiori_rss_client = RssClient.RssClient(db_manager, 'reportiori.ge', '0001.01.01 01:01:01',
                                                    reportiori_parser, 1, logger)
        rss_clients.append(reportiori_rss_client)

        # https://sova.news/feed/
        sovanews_parser = SovanewsParser.SovanewsParser(logger)
        sovanews_rss_client = RssClient.RssClient(db_manager, 'sova.news', '0001.01.01 01:01:01', sovanews_parser,
                                                  1, logger)
        rss_clients.append(sovanews_rss_client)

        # https://sputnik-georgia.ru/export/rss2/archive/index.xml
        sputnikgeorgia_parser = SputnikgeorgiaParser.SputnikgeorgiaParser(logger)
        sputnikgeorgia_rss_client = RssClient.RssClient(db_manager, 'sputnik-georgia.ru', '0001.01.01 01:01:01',
                                                        sputnikgeorgia_parser, 1, logger)
        rss_clients.append(sputnikgeorgia_rss_client)

        # http://www.tabula.ge/rss
        tabula_parser = TabulaParser.TabulaParser(logger)
        tabula_rss_client = RssClient.RssClient(db_manager, 'www.tabula.ge', '0001.01.01 01:01:01', tabula_parser,
                                                1, logger)
        rss_clients.append(tabula_rss_client)

    def add_ukrainian_agencies(self, rss_clients, logger):

        # www.aif.ua
        # http://www.aif.ua/rss/all.php
        aifua_parser = AifuaParser.AifuaParser(logger)
        aifua_rss_client = RssClient.RssClient(db_manager, 'www.aif.ua', '0001.01.01 01:01:01', aifua_parser, 1, logger)
        rss_clients.append(aifua_rss_client)

        # www.capital.ua
        # https://www.capital.ua/rss/rss_public_ru.xml
        capitalua_parser = CapitaluaParser.CapitaluaParser(logger)
        capitalua_rss_client = RssClient.RssClient(db_manager, 'www.capital.ua', '0001.01.01 01:01:01',
                                                   capitalua_parser, 1, logger)
        rss_clients.append(capitalua_rss_client)

        # day.kyiv.ua
        # http://day.kiev.ua/uk/news-rss.xml
        daykyivua_parser = DaykyivuaParser.DaykyivuaParser(logger)
        daykyivua_rss_client = RssClient.RssClient(db_manager, 'day.kyiv.ua', '0001.01.01 01:01:01',
                                                   daykyivua_parser, 1, logger)
        rss_clients.append(daykyivua_rss_client)

        # www.dialog.ua
        # https://www.dialog.ua/all.rss
        dialogua_parser = DialoguaParser.DialoguaParser(logger)
        dialogua_rss_client = RssClient.RssClient(db_manager, 'www.dialog.ua', '0001.01.01 01:01:01',
                                                  dialogua_parser, 1, logger)
        rss_clients.append(dialogua_rss_client)

        # fakty.com.ua
        # https://fakty.com.ua/feed/
        factycomua_parser = FactycomuaParser.FactycomuaParser(logger)
        factycomua_rss_client = RssClient.RssClient(db_manager, 'fakty.com.ua', '0001.01.01 01:01:01',
                                                    factycomua_parser, 1, logger)
        rss_clients.append(factycomua_rss_client)

        # fakty.ua
        # https://fakty.ua/rss_feed/all
        facty_parser = FactyuaParser.FactyuaParser(logger)
        facty_rss_client = RssClient.RssClient(db_manager, 'fakty.ua', '0001.01.01 01:01:01',
                                               facty_parser, 1, logger)
        rss_clients.append(facty_rss_client)

        # news.finance.ua
        # https://news.finance.ua/ru/rss
        financeua_parser = FinanceuaParser.FinanceuaParser(logger)
        financeua_rss_client = RssClient.RssClient(db_manager, 'news.finance.ua', '0001.01.01 01:01:01',
                                                   financeua_parser, 1, logger)
        rss_clients.append(financeua_rss_client)

        # for-ua.com
        # https://for-ua.com/rss
        forua_parser = ForuaParser.ForuaParser(logger)
        forua_rss_client = RssClient.RssClient(db_manager, 'for-ua.com', '0001.01.01 01:01:01', forua_parser, 1, logger)
        rss_clients.append(forua_rss_client)

        # fraza.ua
        # https://fraza.ua/rss/
        frazaua_parser = FrazauaParser.FrazauaParser(logger)
        frazaua_rss_client = RssClient.RssClient(db_manager, 'fraza.ua', '0001.01.01 01:01:01',
                                                 frazaua_parser, 1, logger)
        rss_clients.append(frazaua_rss_client)

        # gazeta.ua
        # https://gazeta.ua/rss
        # gazetaua_parser = ZnakParser.ZnakParser(logger)
        # gazetaua_rss_client = RssClient.RssClient(db_manager, 'gazeta.ua', '0001.01.01 01:01:01',
        # gazetaua_parser, 1, logger)
        # rss_clients.append(gazetaua_rss_client)

        # www.golos.com.ua
        # goloscomua_parser = ZnakParser.ZnakParser(logger)
        # goloscomua_rss_client = RssClient.RssClient(db_manager, 'www.golos.com.ua', '0001.01.01 01:01:01',
        # goloscomua_parser, 1, logger)
        # rss_clients.append(goloscomua_rss_client)

        # golos.ua
        # https://golos.ua/rss
        golosua_parser = GolosuaParser.GolosuaParser(logger)
        golosua_rss_client = RssClient.RssClient(db_manager, 'golos.ua', '0001.01.01 01:01:01',
                                                 golosua_parser, 1, logger)
        rss_clients.append(golosua_rss_client)

        # interfax.com.ua
        # https://interfax.com.ua/news/last.rss
        interfaxcomua_parser = InterfaxcomuaParser.InterfaxcomuaParser(logger)
        interfaxcomua_rss_client = RssClient.RssClient(db_manager, 'interfax.com.ua', '0001.01.01 01:01:01',
                                                       interfaxcomua_parser, 1, logger)
        rss_clients.append(interfaxcomua_rss_client)

        # ipress.ua
        # https://ipress.ua/rss/export.rss
        ipressua_parser = IpressuaParser.IpressuaParser(logger)
        ipressua_rss_client = RssClient.RssClient(db_manager, 'ipress.ua', '0001.01.01 01:01:01',
                                                  ipressua_parser, 1, logger)
        rss_clients.append(ipressua_rss_client)

        # izvestia.kiev.ua
        # https://izvestia.kiev.ua/rss
        izvestiakievua_parser = IzvestiakievuaParser.IzvestiakievuaParser(logger)
        izvestiakievua_rss_client = RssClient.RssClient(db_manager, 'izvestia.kiev.ua', '0001.01.01 01:01:01',
                                                        izvestiakievua_parser, 1, logger)
        rss_clients.append(izvestiakievua_rss_client)

        # kontrakty.ua
        # http://kontrakty.ua/feed/.ukrnet
        kontrakty_parser = KontraktyParser.KontaktyParser(logger)
        kontrakty_rss_client = RssClient.RssClient(db_manager, 'kontrakty.ua', '0001.01.01 01:01:01',
                                                   kontrakty_parser, 1, logger)
        rss_clients.append(kontrakty_rss_client)

        # korrespondent.net
        # http://k.img.com.ua/rss/ru/all_news2.0.xml
        korrespondent_parser = KorrespondentParser.KorrespondentParser(logger)
        korrespondent_rss_client = RssClient.RssClient(db_manager, 'korrespondent.net', '0001.01.01 01:01:01',
                                                       korrespondent_parser, 1, logger)
        rss_clients.append(korrespondent_rss_client)

        # kp.ua
        # https://kp.ua/rss/feed.xml
        kpua_parser = KpuaParser.KpuaParser(logger)
        kpua_rss_client = RssClient.RssClient(db_manager, 'kp.ua', '0001.01.01 01:01:01', kpua_parser, 1, logger)
        rss_clients.append(kpua_rss_client)

        # kratko-news.com
        # http://kratko-news.com/feed/
        kratkonews_parser = KratkonewsParser.KratkonewsParser(logger)
        kratkonews_rss_client = RssClient.RssClient(db_manager, 'kratko-news.com', '0001.01.01 01:01:01',
                                                    kratkonews_parser, 1, logger)
        rss_clients.append(kratkonews_rss_client)

        # nbnews.com.ua
        # https://nbnews.com.ua/feed/
        nbnewscomua_parser = NbnewscomuaParser.NbnewscomuaParser(logger)
        nbnewscomua_rss_client = RssClient.RssClient(db_manager, 'nbnews.com.ua', '0001.01.01 01:01:01',
                                                     nbnewscomua_parser, 1, logger)
        rss_clients.append(nbnewscomua_rss_client)

        # newsoboz.org
        # http://newsoboz.org/static/rss/newsline.rss.xml
        newsoboz_parser = NewsobozParser.NewsobozParser(logger)
        newsoboz_rss_client = RssClient.RssClient(db_manager, 'newsoboz.org', '0001.01.01 01:01:01',
                                                  newsoboz_parser, 1, logger)
        rss_clients.append(newsoboz_rss_client)

        # nua.in.ua
        # https://nua.in.ua/feed/
        nuainua_parser = NuainuaParser.NuainuaParser(logger)
        nuainua_rss_client = RssClient.RssClient(db_manager, 'nua.in.ua', '0001.01.01 01:01:01',
                                                 nuainua_parser, 1, logger)
        rss_clients.append(nuainua_rss_client)

        # nv.ua
        # https://nv.ua/rss/all.xml
        nvua_parser = NvuaParser.NvuaParser(logger)
        nvua_rss_client = RssClient.RssClient(db_manager, 'nv.ua', '0001.01.01 01:01:01', nvua_parser, 1, logger)
        rss_clients.append(nvua_rss_client)

        # www.obozrevatel.com
        # https://www.obozrevatel.com/rss.xml
        obozrevatel_parser = ObozrevatelParser.ObozrevatelParser(logger)
        obozrevatel_rss_client = RssClient.RssClient(db_manager, 'www.obozrevatel.com', '0001.01.01 01:01:01',
                                                     obozrevatel_parser, 1, logger)
        rss_clients.append(obozrevatel_rss_client)

        # Error in feed formating.
        # odessa-life.od.ua
        # https://odessa-life.od.ua/feed
        # odessalife_parser = OdessalifeParser.OdessalifeParser(logger)
        # odessalofe_rss_client = RssClient.RssClient(db_manager, 'odessa-life.od.ua', '0001.01.01 01:01:01',
        #                                             odessalife_parser, 1, logger)
        #rss_clients.append(odessalofe_rss_client)

        # 112.ua
        # https://112.ua/rsslist
        oneonetwo_parser = OneonetwoParser.OneonetwoParser(logger)
        oneonetwo_rss_client = RssClient.RssClient(db_manager, '112.ua', '0001.01.01 01:01:01',
                                                   oneonetwo_parser, 1, logger)
        rss_clients.append(oneonetwo_rss_client)

        # pressorg24.com
        # http://pressorg24.com/news.xml
        pressorg_parser = PressorgParser.PressorgParser(logger)
        preeorg_rss_client = RssClient.RssClient(db_manager, 'pressorg24.com', '0001.01.01 01:01:01',
                                                 pressorg_parser, 1, logger)
        rss_clients.append(preeorg_rss_client)

        # www.sobytiya.info
        # http://www.sobytiya.info/rssFeed/
        sobytiya_parser = SobytiyaParser.SobitiyaParser(logger)
        sobytiaorg_rss_client = RssClient.RssClient(db_manager, 'www.sobytiya.info', '0001.01.01 01:01:01',
                                                    sobytiya_parser, 1, logger)
        rss_clients.append(sobytiaorg_rss_client)

        # tsn.ua
        # https://tsn.ua/rss/full.rss
        tsn_parser = TsnParser.TsnParser(logger)
        tsn_rss_client = RssClient.RssClient(db_manager, 'tsn.ua', '0001.01.01 01:01:01', tsn_parser, 1, logger)
        rss_clients.append(tsn_rss_client)

        # ukranews.com
        # https://ukranews.com/rss-gen
        ukranews_parser = UkranewsParser.UkranewsParser(logger)
        ukranews_rss_client = RssClient.RssClient(db_manager, 'ukranews.com', '0001.01.01 01:01:01',
                                                  ukranews_parser, 1, logger)
        rss_clients.append(ukranews_rss_client)

        # www.ukrinform.ua
        # https://www.ukrinform.ua/block-lastnews
        # ukrinform_parser = ZnakParser.ZnakParser(logger)
        # znak_rss_client = RssClient.RssClient(db_manager, 'www.ukrinform.ua', '0001.01.01 01:01:01',
        # ukrinform_parser, 1, logger)
        # rss_clients.append(znak_rss_client)

        # vesti-ua.net
        # https://vesti-ua.net/engine/rss.php
        vestiua_parser = VestiuaParser.VestiuaParser(logger)
        vestiua_rss_client = RssClient.RssClient(db_manager, 'vesti-ua.net', '0001.01.01 01:01:01',
                                                 vestiua_parser, 1, logger)
        rss_clients.append(vestiua_rss_client)

        # vesti-ukr.com
        # https://t.me/vestiukr
        # vestiukr_parser = ZnakParser.ZnakParser(logger)
        # vestiukr_rss_client = RssClient.RssClient(db_manager, 'vesti-ukr.com', '0001.01.01 01:01:01',
        # vestiukr_parser, 1, logger)
        # rss_clients.append(vestiukr_rss_client)

        # visti.pro
        # http://visti.pro/rss.xml
        vistipro_parser = VistiproParser.VistiproParser(logger)
        vistipro_rss_client = RssClient.RssClient(db_manager, 'visti.pro', '0001.01.01 01:01:01',
                                                  vistipro_parser, 1, logger)
        rss_clients.append(vistipro_rss_client)

        # vlasti.net
        # http://vlasti.net/yandex-feed
        vlastinet_parser = VlastinetParser.VlastinetParser(logger)
        vlastinet_rss_client = RssClient.RssClient(db_manager, 'vlasti.net', '0001.01.01 01:01:01',
                                                   vlastinet_parser, 1, logger)
        rss_clients.append(vlastinet_rss_client)

        # zaxid.net
        # https://zaxid.net/home/showRss.do
        zahid_parser = ZahidParser.ZahidParser(logger)
        zahid_rss_client = RssClient.RssClient(db_manager, 'zaxid.net', '0001.01.01 01:01:01', zahid_parser, 1, logger)
        rss_clients.append(zahid_rss_client)

        # znaj.ua
        # https://znaj.ua/feed/rss2.xml
        znaj_parser = ZnajParser.ZnajParser(logger)
        znaj_rss_client = RssClient.RssClient(db_manager, 'znaj.ua', '0001.01.01 01:01:01', znaj_parser, 1, logger)
        rss_clients.append(znaj_rss_client)


if __name__ == "__main__":
    config_file = "e:\\Projects\\spiderstat\\config.json"
    logger = Logger.Logger(config_file)
    db_manager = DbManager.DbManager(config_file, logger)
    rss_clients = []

    gather_manager = GatherManager(rss_clients, db_manager, 30 * 60, logger)
    gather_manager.add_russian_agencies(rss_clients, logger)
    gather_manager.add_azerbaijani_agencies(rss_clients, logger)
    gather_manager.add_georgian_agencies(rss_clients, logger)
    gather_manager.add_ukrainian_agencies(rss_clients, logger)

    try:
        gather_manager.gather()
    except Exception as e:
            message = logger.make_message("Error in GatherManager", e, "")
            logger.write_message(message)
