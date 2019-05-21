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
    for a in ['articles/articles1.csv', 'articles/articles2.csv', 'articles/articles3.csv']:
        articles += read_csv_file(a)
    return articles


def read_file(file_name):
    with open(file_name, 'r') as f:
        res = f.read()
    return res


def write_to_file(file_name, content):
    with open(file_name, 'w') as f:
        f.write(content)