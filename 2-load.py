import csv
import sys
import plyvel
import json
import gzip
import shutil


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


shutil.rmtree("imdb.lvldb", ignore_errors=True)

db = plyvel.DB("imdb.lvldb", create_if_missing=True)

limit = None
if len(sys.argv) > 1:
    limit = int(sys.argv[1])

actors = db.prefixed_db(b"actors/")
actors_by_title = db.prefixed_db(b"idx_actors_by_title/")
titles = db.prefixed_db(b"titles/")

for item in read_titles(limit):
    key = bytes(item["tconst"], encoding="utf8")
    data = bytes(json.dumps(item), encoding="utf8")

    titles.put(key, data)


for item in read_names(limit):
    key = bytes(item["nconst"], encoding="utf8")
    data = bytes(json.dumps(item), encoding="utf8")
    if "knownForTitles" in item and item["knownForTitles"] is not None:
        for title in item["knownForTitles"]:
            idx_key = bytes(title, encoding="utf8") + b"|" + key
            actors_by_title.put(idx_key, key)
    actors.put(key, data)


db.close()
