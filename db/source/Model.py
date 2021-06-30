import json


class Item:
    def __init__(self):
        self.key = ""
        self.value = []

    def NewItem(self, key, value):
        self.key = key
        self.value = json.dumps(value).encode("utf-8")

    def getDictItem(self):
        try:
            return dict(key=self.key, value=json.loads(self.value))
        except Exception as e:
            print(r'[ERR] error Loads JSON')
            print(r'[ERR] db\Model.py line:18 ', e)
