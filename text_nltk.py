# -*- coding: utf-8 -*-
"""
    The text module extracts words from text using punktuation and word tokenizers,
    rejects common stopwords, and lemmatizes each word.
    
    Example:
        >>> from text import lemma_tokenize
    
        >>> lemma_tokenize('100% of your donation funds medical care for patients around the world.')
        ['100', '%', 'donation', 'fund', 'medical', 'care', 'patient', 'around', 'world']

   Author: Dirk Neumann
"""
import nltk
import nltk.tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize.api import StringTokenizer
import numpy as np
import numpy.linalg
import sys

emotion_names = ['happy', 'sad', 'surprised', 'angry', 'fearful', 'disgusted',
                 'rage', 'vigilance', 'ecstasy', 'admiration', 'terror', 'amazement', 'grief', 'loathing',
                 'anger', 'anticipation', 'joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust', 'anger',
                 'annoyance', 'interest', 'serenity', 'acceptance', 'apprehension', 'distraction', 'thoughtful', 'boredom',
                 'aggressiveness', 'optimism', 'love', 'submission', 'awe', 'disapproval', 'remorse', 'contempt',
                 'hate']


def empathy(x, model=None):
    # emotion_names = ['happy', 'sad', 'surprised', 'angry', 'fearful',
    # 'disgusted'] #anger disgust fear joy sadness surprise
    d = {}
    for a_emotion in emotion_names:
        print >>sys.stderr, a_emotion
        d[a_emotion] = np.dot(vectors(a_emotion, model=model)[1:], x[
                              1:]) / numpy.linalg.norm(vectors(a_emotion, model=model)[1:]) / numpy.linalg.norm(x[1:])
    return d


def lemma_tokenize(paragraph):
    lmtzr = WordNetLemmatizer()
    try:
        return [lmtzr.lemmatize(word).lower() for sentence in tokenize(paragraph) for word in sentence]
    except LookupError:
        nltk.download('wordnet')
        return [lmtzr.lemmatize(word).lower() for sentence in tokenize(paragraph) for word in sentence]


def mean_vector(paragraph, model=None):
    return np.nanmean([vectors(w, model=model) for w in lemma_tokenize(paragraph)], axis=0)


def stopwords():
    try:
        stop_words = stopwords.stop_words
    except AttributeError:
        try:
            stop_words = nltk.corpus.stopwords.words('english')
        except LookupError:
            nltk.download('stopwords')
            stop_words = nltk.corpus.stopwords.words('english')
        stop_words.extend(
            ['-', ':', '.', '\'', '\',', ',', '#', '/', '@', '.,', '(', ')', 'RT', 'I', 'I''m'])
        stopwords.stop_words = stop_words
    return stop_words


def tokenize(paragraph):
    if not paragraph:
        return []

    try:
        detector = tokenize.detector
    except AttributeError:
        try:
            detector = nltk.data.load('tokenizers/punkt/english.pickle')
        except LookupError:
            nltk.download('punkt')
            detector = nltk.data.load('tokenizers/punkt/english.pickle')
        tokenize.detector = detector

    return [
        [
            word
            for word in nltk.tokenize.word_tokenize(sentence)
            if word not in stopwords()
        ]
        for sentence in detector.tokenize(paragraph.strip())
    ]

'''
def vectors(x):
    try:
        v = vectors.vectors
    except AttributeError:
        from gzip import GzipFile
        vectors.vectors = {}
        from gensim.models import Word2Vec
        m = Word2Vec.load('/mnt/data/text8.model')
        for i, word in enumerate(m.vocab):
             vectors.vectors[word] = [1, ] + [float(x) for x in m[word][:25]]

        v = vectors.vectors

    return v[x] if x in v else v.itervalues().next()
'''


def semantic_vector_skip(text, model=None):
    words = lemma_tokenize(text)
    if len(words) == 0:
        return None
    return [x for x in np.asarray(np.nanmean([vectors(w, model=model) for w in words], axis=0))]


def vectors(x, model=None):
    if not model:
        model = 'vectors_50d'
    try:
        v = vectors.vectors
    except AttributeError:
        vectors.vectors = {}

    try:
        v = vectors.vectors[model]
    except KeyError:
        vectors.vectors[model] = {}

        from gzip import GzipFile
        # for i, row in enumerate(GzipFile('/mnt/data/GoogleNews-vectors-negative300.txt.gz')):
        #    if i > 0:
        filename = '/mnt/data/%s.txt.gz' % model
        print >>sys.stderr, 'Loading %s...' % filename
        for row in GzipFile(filename):
            vectors.vectors[model][
                row.split(' ')[0]] = [1, ] + map(float, row.split(' ')[1:26])

        v = vectors.vectors[model]

    return v[x] if x in v else ([np.nan, ] * len(vectors('the')))
