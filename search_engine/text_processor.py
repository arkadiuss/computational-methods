from nltk.tokenize import word_tokenize


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
