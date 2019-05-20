from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def remove_characters_non_alpha(article):
    return ''.join(c for c in article if c.isalpha() or c == ' ')


def prepare_text_old(article):
    return remove_characters_non_alpha(article).lower().split(' ')


def bag_of_words(text):
    words = {}
    for i in text:
        words[i] = words.get(i, 0) + 1
    return words


def prepare_text(text):
    return word_tokenize(text)


def stem_words(words):
    stemmer = PorterStemmer()
    return list(set([stemmer.stem(w) for w in words]))


def remove_stop_words(words):
    stop_words = set(stopwords.words('english'))
    return [w for w in words if w not in stop_words]


def remove_punctuation(words):
    return [w for w in words if w.isalpha()]


def filter_words(words_vector):
    words_vector = remove_punctuation(words_vector)
    words_vector = stem_words(words_vector)
    words_vector = remove_stop_words(words_vector)
    return words_vector
