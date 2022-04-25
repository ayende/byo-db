import json
import os
import sys
import plyvel


db = plyvel.DB("imdb.lvldb", create_if_missing=False)
key = bytes(sys.argv[1], encoding="utf8")

titles = db.prefixed_db(b"titles/")
actors = db.prefixed_db(b"actors")
actors_by_title = db.prefixed_db(b"idx_actors_by_title/")

titleVal = titles.get(key)
if titleVal is None:
    print(b"Unknown id " + key)
    os._exit(1)

title = json.loads(titleVal)

print(title["primaryTitle"])

print("Actors: ")

for _, actorId in actors_by_title.iterator(prefix=key + b"|"):
    actorVal = actors.get(actorId)
    if actorVal is None:
        print(b" - missing " + actorId)
        continue

    actor = json.loads(actorVal)
    print(b" - " + actor["primaryName"])
