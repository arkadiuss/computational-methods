import numpy as np
from scipy import sparse
from text_processor import bag_of_words, prepare_text
from common import read_file, write_to_file

def prepare_phrase(phrase, words):
    p = prepare_text(phrase)
    return phrase


print("Loading matrix...")
search_matrix = sparse.load_npz('matrix_compressed_sparse.npz')
print("Matrix loaded: " + str(search_matrix.shape))

print("Loading words...")
words = read_file('words.txt')
print("Words loaded: " + str(words))


print("Type search phrase:")
phrase = input()
phrase = prepare_phrase(phrase, words)
print(phrase)
