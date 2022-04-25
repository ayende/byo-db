import json
import os
import sys
import plyvel


db = plyvel.DB("imdb.lvldb", create_if_missing=False)
term = sys.argv[1].lower()

titles = db.prefixed_db(b"titles/")

print("Matches for " + term)

for k, v in titles:
    title = json.loads(v)
    loweCareTitle = title["primaryTitle"].lower()
    if term in loweCareTitle:
        print(title["primaryTitle"])
