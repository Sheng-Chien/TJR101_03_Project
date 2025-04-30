from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# 建立連線
user = "Eta"
pw = "PassWord"
ip = "104.199.214.113"
port = "27017"
database = "EtaDB"
try:
    client = MongoClient(f"mongodb://{user}:{pw}@{ip}:{port}/?authSource={database}", serverSelectionTimeoutMS=3000)
    client.admin.command("ping")  # 強制測試連線
    print("✅ MongoDB connected!")
except ServerSelectionTimeoutError as e:
    print("❌ 無法連線到 MongoDB：", e)

# 選擇資料庫
db = client[database]

# 選擇集合（相當於SQL裡的表格）
collection = db['hello']

# 測試插入一筆資料
collection.insert_one({"name": "Alice", "age": 25})

# 測試查詢
result = collection.find_one({"name": "Alice"})
print(result)
