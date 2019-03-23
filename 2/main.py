import numpy as np
import os
import csv
import networkx as nx


def import_from_file(file):
    records = []

    with open(file, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            records.append(row)
    #map(records


G = nx.Graph()
import_from_file("soc-sign-bitcoinalpha.csv")


