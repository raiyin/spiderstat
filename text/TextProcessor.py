# Библиотека для работы с предупреждениями
import warnings
import pymorphy2
from nltk.corpus import stopwords
import nltk

warnings.filterwarnings('ignore')  # Игнорировать предупреждения


class TextProcessor:

    def __init__(self):
        self.stop_words = set(stopwords.words('russian'))
        nltk.download('stopwords')

    def remove_punctuation_marks(self, text):
        text = text.replace('\\', ' ')
        text = text.replace('`', ' ')
        text = text.replace('*', ' ')
        text = text.replace('_', ' ')
        text = text.replace('{', ' ')
        text = text.replace('}', ' }')
        text = text.replace('[', ' ')
        text = text.replace(']', ' ')
        text = text.replace('(', ' ')
        text = text.replace(')', ' ')
        text = text.replace('>', ' ')
        text = text.replace('<', ' ')
        text = text.replace('#', ' ')
        text = text.replace('+', ' ')
        text = text.replace('-', ' ')
        text = text.replace('.', ' ')
        text = text.replace(',', ' ')
        text = text.replace('!', ' ')
        text = text.replace('?', ' ')
        text = text.replace('$', ' ')
        text = text.replace('—', ' ')
        text = text.replace('«', ' ')
        text = text.replace('»', ' ')
        return text

    def clean(self, text):

        # Очистка текста
        # text = text.lower()
        # text = text.replace('[\t\n\r\f\v.*$]', ' ')
        # text = text.replace('-', ' ')
        # text = text.replace('[^йцукенгшщзхъфывапролджэячсмитьбюё0-9A-Za-z ]+', '')
        text = self.remove_punctuation_marks(text)

        # Нормализация текста
        morph = pymorphy2.MorphAnalyzer()
        text = ' '.join([morph.parse(item)[0].normal_form for item in str(text).split(' ')])

        # Удаление стоп-слов
        text = ' '.join([w for w in text.split() if w not in self.stop_words])
        return text


if __name__ == "__main__":
    text_processor = TextProcessor()
    text_dirty = "В качестве затравки посмотрим, что из себя представляют публикации в самом общем виде. Выведем 50 " \
                 "наиболее частотных слов, которые употребляли журналисты Ленты с 1999 по 2017 год, в виде облака " \
                 "тегов. "
    text_clean = text_processor.clean(text_dirty)
    print(text_clean)
