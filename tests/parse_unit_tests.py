import unittest
from parsing import LifeParser
from parsing import RbcParser
from parsing import LentaParser
from parsing import MailParser
from parsing import NewsruParser
from parsing import BbcParser
from parsing import RgParser
from parsing import IzParser
from parsing import PravdaParser


class TestStringMethods(unittest.TestCase):

    def test_rbc_parser(self):
        my_parser = RbcParser.RbcParser()
        success, article = my_parser.parse('https://www.rbc.ru/rbcfreenews/5bc8acd19a7947257ed65f69')
        self.assertNotEqual(article, '')

    def test_lenta_parser(self):
        my_parser = LentaParser.LentaParser()
        success, article = my_parser.parse('https://lenta.ru/news/2018/10/18/40n6/')
        self.assertNotEqual(article, '')

    def test_life_parser(self):
        my_parser = LifeParser.LifeParser()
        success, article = my_parser.parse('https://life.ru/1164883')
        self.assertNotEqual(article, '')

    def test_life_parser_1(self):
        my_parser = LifeParser.LifeParser()
        success, article = my_parser.parse('https://life.ru/t/%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F/1165006/krushieniie_tsarskogho_poiezda_koghda_russkii_impierator_poviol_siebia_kak_nastoiashchii_muzhik')
        self.assertNotEqual(article, '')

    def test_mail_parser(self):
        my_parser = MailParser.MailParser()
        success, article = my_parser.parse('https://news.mail.ru/society/35093981/')
        self.assertNotEqual(article, '')

    def test_newsru_parser(self):
        my_parser = NewsruParser.NewsruParser()
        success, article = my_parser.parse('https://www.newsru.com/world/18oct2018/volkerussnctns.html')
        self.assertNotEqual(article, '')

    def test_bbc_parser(self):
        my_parser = BbcParser.BbcParser()
        success, article = my_parser.parse('https://www.bbc.com/russian/news-45906295')
        self.assertNotEqual(article, '')

    def test_rg_parser(self):
        my_parser = RgParser.RgParser()
        success, article = my_parser.parse('https://rg.ru/2018/10/18/cb-nameren-otmenit-bankovskoe-rabstvo.html')
        self.assertNotEqual(article, '')

    def test_iz_parser(self):
        my_parser = IzParser.IzParser()
        success, article = my_parser.parse('https://iz.ru/805117/georgii-oltarzhevskii/vzryv-pokrovov-kto-podorval-linkor-novorossiisk')
        self.assertNotEqual(article, '')

    def test_pravda_parser(self):
        my_parser = PravdaParser.PravdaParser()
        success, article = my_parser.parse('https://zoo.pravda.ru/news/zoouseful/18-10-2018/1396417-birds-0/')
        self.assertNotEqual(article, '')


if __name__ == '__main__':
    unittest.main()
