import csv
import sys

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


print("Reading articles...")
articles = read_articles()[:10000]

print("Preparing...")
for i in range(len(articles)):
    #id = articles[i][0]
    articles[i] = prepare_article(articles[i][-1])
    #f.write("{0}, {1}\n".format(id, articles[i]))


print("Creating word vector...")
#words_vector = create_words_vector(articles)
#write_to_file('words.txt', ",".join(words_vector))
print("Cached")
words_vector = set(read_file('words.txt').split(','))
print(len(words_vector))