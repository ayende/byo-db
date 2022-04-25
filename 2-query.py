import json
import os
import sys
import plyvel


db = plyvel.DB("imdb.lvldb", create_if_missing=False)
titleId = bytes(sys.argv[1], encoding="utf8")


titles = db.prefixed_db(b"titles/")
actors_by_title = db.prefixed_db(b"idx_actors_by_title/")
actors = db.prefixed_db(b"actors/")

titleVal = titles.get(titleId)
title = json.loads(titleVal)

print(title["primaryTitle"])

for k, v in actors_by_title.iterator(prefix=titleId):
    actorVal = actors.get(v)
    actor = json.loads(actorVal)
    print(" - " + actor["primaryName"])
