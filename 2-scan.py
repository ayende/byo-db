import json
import os
import sys
import plyvel


db = plyvel.DB("imdb.lvldb", create_if_missing=False)
titleId = bytes(sys.argv[1], encoding="utf8")


titles = db.prefixed_db(b"titles/")
actors = db.prefixed_db(b"actors/")

titleVal = titles.get(titleId)
title = json.loads(titleVal)

print(title["primaryTitle"])

titleIdStr = str(titleId, encoding="utf8")

for k, v in actors:
    actor = json.loads(v)
    actorTitles = actor["knownForTitles"]
    if actorTitles is not None and titleIdStr in actorTitles:
        print(" - " + actor["primaryName"])
