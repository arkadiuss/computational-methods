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
        articles.append(read_csv_file(a))
    return articles


def remove_characters(article):
    return ''.join(c for c in article if c.isalpha() or c == ' ')


def bow(article):
    return [[x, article.count(x)] for x in article.split()]


article1 = remove_characters(read_articles()[0][-1][-1])
print(bow(article1))