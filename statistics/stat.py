from gensim import corpora, models


class Stat:
    def __init__(self):
        pass

    def dict_count(self, text):
        words = text.split()
        dictionary = corpora.Dictionary(words)
        corpus = dictionary.doc2bow(words)

        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        model = models.ldamodel.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=1,
                                         passes=30, alpha=1.25, eta=1.25)
        print(model)


if __name__ == '__main__':
    text = "В качестве затравки посмотрим, что из себя представляют публикации в самом общем виде. Выведем 50 " \
                 "наиболее частотных слов, которые употребляли журналисты Ленты с 1999 по 2017 год, в виде облака " \
                 "тегов. "
    stat = Stat()
    stat.dict_count(text)
