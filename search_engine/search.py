import numpy as np
from scipy import sparse
from text_processor import bag_of_words, prepare_text, filter_words
from common import read_file


def prepare_phrase(phrase, words):
    p = filter_words(prepare_text(phrase))
    bow = bag_of_words(p)
    return np.array([bow.get(w, 0) for w in words])


def correlation(phrase_words, article_words):
    return phrase_words.T @ article_words / (np.linalg.norm(phrase_words) * np.linalg.norm(article_words))


def match(phrase_words, search_matrix):
    matches = []
    for i, a_w in enumerate(search_matrix):
        matches.append((i, correlation(phrase_words, a_w)))
    matches.sort(key=lambda x: x[1], reverse = True)
    return matches[:10]


print("Loading words...")
words = np.array(read_file('words.txt').split(','))
words.sort()
print("Words loaded: " + str(words))

print("Loading matrix...")
search_matrix = sparse.load_npz('matrix.npz').toarray()
print("Matrix loaded: " + str(search_matrix.shape))

print("Loading articles...")
articles = [a.split(',') for a in read_file('p_articles.txt').split('\n')]

print("Type search phrase:")
phrase = input()
phrase_words = prepare_phrase(phrase, words)
for i, c in match(phrase_words, search_matrix):
    print(c, articles[i])