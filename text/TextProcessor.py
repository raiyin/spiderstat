# Библиотека для работы с предупреждениями
import warnings
warnings.filterwarnings('ignore')  # Игнорировать предупреждения

# Библиотеки для работы с данными
import pandas as pd
import numpy as np

# Библиотеки для работы с текстом
import pymorphy2
from nltk.corpus import stopwords
from gensim import corpora, models

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer

from sklearn.linear_model import LogisticRegression

# import xgboost as xgb

from sklearn.metrics import f1_score, classification_report, confusion_matrix, accuracy_score

from scipy.stats import pearsonr, chisquare

from keras.preprocessing.text import one_hot
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Embedding, Dense, LSTM
from keras.callbacks import EarlyStopping, ModelCheckpoint


from gensim.models import Word2Vec
from sklearn.decomposition import PCA


import time
import pickle
import nltk

class TextProcessor:

    def clean(self, text):
        nltk.download('stopwords')

        # Очистка текста
        text = text.lower()
        text = text.replace('[\t\n\r\f\v.*$]', '')
        text = text.replace('-', ' ')
        text = text.replace('[^йцукенгшщзхъфывапролджэячсмитьбюё0-9A-Za-z ]+', '')

        # Нормализация текста
        morph = pymorphy2.MorphAnalyzer()
        text = ' '.join([morph.parse(item)[0].normal_form for item in str(text).split(' ')])

        # Удаление стоп-слов
        stop_words = set(stopwords.words('russian'))
        text = ' '.join([w for w in text.split() if w not in stop_words])
        return text


if __name__ == "__main__":
    text_processor = TextProcessor()
    text_dirty = "В качестве затравки посмотрим, что из себя представляют публикации в самом общем виде. Выведем 50 " \
                 "наиболее частотных слов, которые употребляли журналисты Ленты с 1999 по 2017 год, в виде облака " \
                 "тегов. "
    text_clean = text_processor.clean(text_dirty)
    print(text_clean)
