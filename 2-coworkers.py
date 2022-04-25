import json
import os
import sys
import plyvel


db = plyvel.DB("imdb.lvldb", create_if_missing=False)
actorId = bytes(sys.argv[1], encoding="utf8")


titles = db.prefixed_db(b"titles/")
actors_by_title = db.prefixed_db(b"idx_actors_by_title/")
actors = db.prefixed_db(b"actors/")

actorVal = actors.get(actorId)
actor = json.loads(actorVal)
print(actor["primaryName"])

actorTitles = actor["knownForTitles"]
coworkers = []
if actorTitles is not None:
    for title in actorTitles:
        for k, v in actors_by_title.iterator(prefix=bytes(title, encoding="utf8")):
            coworkers.append(v)

print("Coworkers:")

for coworkerId in set(coworkers):
    if coworkerId == actorId:
        continue
    coworkerVal = actors.get(coworkerId)
    coworker = json.loads(coworkerVal)
    print(" - " + coworker["primaryName"])
