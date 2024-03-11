from pymongo import MongoClient

uri = "mongodb://root:root@localhost/"
client = MongoClient(uri)

try:
  client.admin.command('ping')
  # print(client.list_database_names())
except Exception as e:
  print(e)
  exit()

# db = client["poc"]
# co = db["products_product"]

# print(db)
# print(co)

for item in client["poc"]["products_product"].find():
  print(item)