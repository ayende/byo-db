import csv
import sys
import json
import gzip
import shutil
import database


def split(dic, name):
    if name in dic and dic[name] != None:
        dic[name] = dic[name].split(",")


def set(dic, name, val):
    if val == "\\N":
        dic[name] = None
    else:
        dic[name] = val


def read_names(max=None):
    count = 0
    with gzip.open("name.basics.tsv.gz", "rt") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        cols = next(reader)
        for line in reader:
            dic = {}
            for i in range(len(cols)):
                if i < len(line):
                    set(dic, cols[i], line[i])

            split(dic, "primaryProfession")
            split(dic, "knownForTitles")
            yield dic
            count = count + 1
            if max is not None and count >= max:
                break


def read_titles(max=None):
    count = 0
    with gzip.open("title.basics.tsv.gz", "rt") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        cols = next(reader)
        for line in reader:
            dic = {}
            for i in range(len(cols)):
                if i < len(line):
                    set(dic, cols[i], line[i])
            split(dic, "genres")
            yield dic
            count = count + 1
            if max is not None and count >= max:
                break


shutil.rmtree("data", ignore_errors=True)

db = database.Database("data")

limit = None
if len(sys.argv) > 1:
    limit = int(sys.argv[1])


for item in read_titles(limit):
    key = bytes(item["tconst"], encoding="utf8")
    data = bytes(json.dumps(item), encoding="utf8")

    db.put(key, data)


for item in read_names(limit):
    key = bytes(item["nconst"], encoding="utf8")
    data = bytes(json.dumps(item), encoding="utf8")
    db.put(key, data)
