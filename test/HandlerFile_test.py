
import json
import sys

sys.path.insert(1, '.')

from db.source.Handler import DBHandler


print(DBHandler().selectFile("topic"))
dbIns = DBHandler()

item = dict(name="abc", c="nnn")
# print(json.dumps(item))
# dbIns.writeItem("topic", 1, json.dumps(item))
rows = dbIns.readTable("topic")
print(json.loads(rows["1"])["name"])

