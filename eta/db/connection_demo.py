from pymongo import MongoClient

# 建立連線
user = "Eta"
pw = "PassWord"
ip = "35.221.213.83"
port = "27017"
database = "EtaDB"
client = MongoClient(f"mongodb://{user}:{pw}@:{port}/?authSource={database}")

# 選擇資料庫
db = client[database]

# 選擇集合（相當於SQL裡的表格）
collection = db['hello']

# 測試插入一筆資料
collection.insert_one({"name": "Alice", "age": 25})

# 測試查詢
result = collection.find_one({"name": "Alice"})
print(result)
