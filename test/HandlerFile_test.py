import sys

sys.path.insert(1, '.')

from db.source.Handler import DBHandler

print(DBHandler().selectFile("topic"))