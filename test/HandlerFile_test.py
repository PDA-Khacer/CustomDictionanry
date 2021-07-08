import json
import sys
from datetime import datetime

sys.path.insert(1, '.')

from db.source.Handler import DBHandler


print(DBHandler().selectFile("topic"))
dbIns = DBHandler()

# ============================ push item
item = dict(Name="develop", CreateAt=str(datetime.now()), CreateBy='admin')
# print(json.dumps(item))
# dbIns.writeItem("topic", "1", item)
# dbIns.writeItem("topic", "5", item)
# dbIns.writeItem("topic", "6", item)

# ============================ get all data
# rows = dbIns.readTable("topic")
# print("rows : ",rows)

# ============================ get Item
# print(json.loads(rows["2"])["name"])
# print("item", dbIns.getItem("topic", "0"))

# ============================ update 
# item = dict(name="update", c="nnn")
# dbIns.updateItem("topic","3", item)

# ============================ delete
# dbIns.deleteitem("topic","5")



dbIns.reIndex("topic")

rows = dbIns.readTable("topic")
print("rows : ",rows)
