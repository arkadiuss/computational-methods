import csv
import sys
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

nltk.download('stopwords')
nltk.download('punkt')

csv.field_size_limit(sys.maxsize)


def read_csv_file(file):
    records = []
    with open(file, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            records.append(row)
    return records


def read_articles():
    articles = []
    for a in ['articles/articles1.csv']:
        articles += read_csv_file(a)
    return articles


def remove_characters(article):
    return ''.join(c for c in article if c.isalpha() or c == ' ')


def prepare_article(article):
    return remove_characters(article).lower().split(' ')


def bag_of_words(article):
    words = {}
    for i in article:
        words[i] = words.get(i, 0) + 1
    return words


def prepare_articles(articles):
    for i in range(len(articles)):
        # id = articles[i][0]
        if i % 1000 == 0:
            print("Tokenized {0} articles".format(i))
        articles[i] = word_tokenize(articles[i][-1])
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


def read_file(file_name):
    with open(file_name, 'r') as f:
        res = f.read()
    return res


def write_to_file(file_name, content):
    with open(file_name, 'w') as f:
        f.write(content)


def stem_words(words):
    stemmer = PorterStemmer()
    return {stemmer.stem(w) for w in words}


def remove_stop_words(words):
    stop_words = set(stopwords.words('english'))
    return [w for w in words if w not in stop_words]


def remove_punctuation(words):
    return [w for w in words if w.isalpha()]


print("Reading articles...")
articles = read_articles()[1:10000]

print("Preparing...")
# articles = prepare_articles(articles)
# articles_str = [",".join(a) for a in articles]
# write_to_file('p_articles.txt', "\n".join(articles_str))
print("Cached")
articles = [a.split(',') for a in read_file('p_articles.txt').split('\n')]

print("Creating word vector...")
# words_vector = create_words_vector(articles)
# write_to_file('words.txt', ",".join(words_vector))
print("Cached")
words_vector = set(read_file('words.txt').split(','))
print("There are {0} words".format(len(words_vector)))

print("Removing punctuation")
words_vector = remove_punctuation(words_vector)
print("There are {0} words after removing punctuation".format(len(words_vector)))

print("Stemming...")
words_vector = stem_words(words_vector)
print("There are {0} words after stemming".format(len(words_vector)))

print("Removing stop words")
words_vector = remove_stop_words(words_vector)
print("There are {0} words after removing stop words".format(len(words_vector)))
