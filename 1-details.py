import json
import sys
import plyvel


db = plyvel.DB("imdb.lvldb", create_if_missing=False)
key = bytes(sys.argv[1], encoding="utf8")

val = db.get(key)
dic = json.loads(val)
formatted = json.dumps(dic, indent=4)
print(formatted)


if "knownForTitles" in dic:
    print("Known for titles:")
    for titleId in dic["knownForTitles"]:
        titleVal = db.get(bytes(titleId, encoding="utf8"))
        if titleVal is None:
            print("Title " + titleId + " was not loaded")
            continue

        title = json.loads(titleVal)
        print(" - " + title["primaryTitle"])
