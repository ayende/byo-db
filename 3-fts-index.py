import json
import os
import sys
import plyvel


db = plyvel.DB("imdb.lvldb", create_if_missing=False)

titles = db.prefixed_db(b"titles/")
fst_title = db.prefixed_db(b"idx_fst_title/")


for k, v in titles:
    title = json.loads(v)
    for term in title["primaryTitle"].lower().split():
        cleanedTerm = term.replace(",", "").replace(".", "").replace('"', "")
        fst_title.put(bytes(cleanedTerm, encoding="utf8") + b"|" + k, k)
