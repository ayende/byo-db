import json
import os
import sys
import plyvel


db = plyvel.DB("imdb.lvldb", create_if_missing=False)
term = sys.argv[1].lower()

titles = db.prefixed_db(b"titles/")
fst_title = db.prefixed_db(b"idx_fst_title/")


print("Matches for " + term)

for k, v in fst_title.iterator(prefix=bytes(term, encoding="utf8") + b"|"):
    titleVal = titles.get(v)
    title = json.loads(titleVal)
    print(title["primaryTitle"])
