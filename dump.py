import sys
import plyvel


db = plyvel.DB("imdb.lvldb", create_if_missing=False)

prefix = ""
if len(sys.argv) > 1:
    prefix = sys.argv[1]


for key, value in db.iterator(start=bytes(prefix, encoding="utf8")):
    print(str(key + b" -> " + value[0:120] + b"...", encoding="utf8"))


db.close()
