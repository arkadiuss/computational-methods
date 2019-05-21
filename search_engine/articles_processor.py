import datetime

import numpy as np
import nltk
from scipy import sparse
from scipy.sparse import linalg
from text_processor import bag_of_words, prepare_text, filter_words, stem_words
from common import read_file, write_to_file, read_articles
from collections import Counter

nltk.download('stopwords')
nltk.download('punkt')


def prepare_articles(articles):
    for i in range(len(articles)):
        # id = articles[i][0]
        if i % 1000 == 0:
            print("Tokenized {0} articles".format(i))
        articles[i] = prepare_text(articles[i][-1])
        # f.write("{0}, {1}\n".format(id, articles[i]))
    return articles


def create_words_vector(articles):
    res = set()
    for k, i in enumerate(articles):
        if k % 1000 == 0:
            print("Processed " + str(k) + " articles")
        bow = bag_of_words(i)
        res = res.union(bow.keys())
    return res


def extract_and_process_words(articles):
    print("Creating word vector...")
    words_vector = create_words_vector(articles)
    print("There are {0} words".format(len(words_vector)))

    words_vector = filter_words(words_vector)
    words_vector.sort()

    return words_vector


def as_sprase_matrix(words, articles):
    indexed_words = {w: i for i, w in enumerate(words)}
    rs = []
    cs = []
    data = []
    for k, a in enumerate(articles):
        if k%1000 == 0:
            print("{0} articles added to matrix".format(k))
        bow = bag_of_words(stem_words(a))
        #matrix[k, :] = ([bow.get(w, 0) for i, w in enumerate(words)])
        for w, c in bow.items():
            if indexed_words.get(w) is not None and c > 0:
                 rs.append(k)
                 cs.append(indexed_words[w])
                 data.append(c)
    print("All added")
    matrix = sparse.csr_matrix((data, (rs, cs)), (len(articles), len(words)), dtype=float)
    print("Sparse matrix created")
    return matrix


def idf(words_matrix):
    N = words_matrix.shape[0]
    c = Counter(words_matrix.nonzero()[1])
    print(datetime.datetime.now())
    print("Counter finished")
    dtf = np.log(N*np.array([1/c[i] for i in range(words_matrix.shape[1])]))
    return sparse.csr_matrix(words_matrix) @ sparse.diags([dtf], [0])


def normalize(words_matrix):
    norm = np.array([1 / (linalg.norm(wr.T)) for wr in words_matrix])
    return sparse.diags([norm], [0]) @ sparse.csr_matrix(words_matrix)


def denoise(word_matrix, denoise_coeff = 100):
    u, s, vt = linalg.svds(word_matrix, denoise_coeff)
    print("SVD counted")
    compressed_matrix = u @ np.diag(s) @ vt
    print("Matrix sparsed")
    return compressed_matrix


print(datetime.datetime.now())
print("Reading articles")
# articles = read_articles()[1:]
size = 10000
articles = read_articles()[1:size+1]
name = 'matrix_'+str(size)
print("There are {0} articles".format(size))

print(datetime.datetime.now())
print("Preparing")
articles = prepare_articles(articles)
articles_str = [",".join(a) for a in articles]
write_to_file('p_articles_{0}.txt'.format(size), "\n".join(articles_str))
# print("Cached")
# articles = [a.split(',') for a in read_file('p_articles_{0}.txt'.format(size)).split('\n')]

print(datetime.datetime.now())
print("Processing words to vector")
words_vector = extract_and_process_words(articles)
write_to_file('words_{0}.txt'.format(size), ",".join(words_vector))
# print("Cached")
# words_vector = read_file('words_{0}.txt'.format(size)).split(',')

print(datetime.datetime.now())
print("Creating sparse matrix")
word_matrix = as_sprase_matrix(words_vector, articles)
sparse.save_npz('{0}.npz'.format(name), word_matrix)
# print("Cached")
# word_matrix = sparse.load_npz('{0}.npz'.format(name))

print(datetime.datetime.now())
print("IDF")
word_matrix = idf(word_matrix)
sparse.save_npz('{0}_idfed.npz'.format(name), word_matrix)
# print("Cached")
# word_matrix = sparse.load_npz('{0}_idfed.npz'.format(name))

print(datetime.datetime.now())
print("Normalization")
word_matrix = normalize(word_matrix)
sparse.save_npz('{0}_normalized.npz'.format(name), word_matrix)
# print("Cached")
# word_matrix = sparse.load_npz('{0}_normalized.npz'.format(name))

print(datetime.datetime.now())
print("SVD")
compressed_matrix_sparse = denoise(word_matrix, denoise_coeff=200)
np.save('{0}_denoised.npy'.format(name), compressed_matrix_sparse)
# sparse.save_npz('{0}_denoised.npz'.format(name), compressed_matrix_sparse)