import json
import sys

sys.path.insert(1, '.')

from db.source.Handler import DBHandler


print(DBHandler().selectFile("topic"))
dbIns = DBHandler()

# item = dict(name="nnn", c="nnn")
# print(json.dumps(item))
# dbIns.writeItem("topic", "6", json.dumps(item))

# ============================ get all data
# rows = dbIns.readTable("topic")
# print("rows : ",rows)

# ============================ get Item
# print(json.loads(rows["2"])["name"])
# print("item", dbIns.getItem("topic", "4"))

# ============================ update 
# item = dict(name="update", c="nnn")
# dbIns.updateItem("topic","3", json.dumps(item))

# ============================ delete
dbIns.deleteitem("topic","6")

rows = dbIns.readTable("topic")
print("rows : ",rows)