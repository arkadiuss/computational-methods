import numpy as np
from nltk import app
from scipy import sparse
from text_processor import bag_of_words, prepare_text, filter_words
from common import read_file
from flask import Flask, request
app = Flask(__name__)


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


size=10000
print("Loading words...")
words = np.array(read_file('words_{0}.txt'.format(size)).split(','))
words.sort()
print("Words loaded: " + str(words))

print("Loading matrix...")
search_matrix = np.load('matrix_{0}_denoised.npy'.format(size))
print("Matrix loaded: " + str(search_matrix.shape))

print("Loading articles...")
articles = [a.split(',') for a in read_file('p_articles_{0}.txt'.format(size)).split('\n')]


def search(phrase):
    phrase_words = prepare_phrase(phrase, words)
    return [(i, c) for i, c in match(phrase_words, search_matrix)]


@app.route("/", methods=['GET'])
def get_searches():
    phrase = request.args.get('phrase')
    return search(phrase)


# print("Type search phrase:")
# phrase = input()
# phrase_words = prepare_phrase(phrase, words)
# for i, c in match(phrase_words, search_matrix):
#     print(c, articles[i])