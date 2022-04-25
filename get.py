import json
import sys
import plyvel


db = plyvel.DB("imdb.lvldb", create_if_missing=False)
key = bytes(sys.argv[1], encoding="utf8")

val = db.get(key)

formatted = json.dumps(json.loads(val), indent=4)
print(formatted)
