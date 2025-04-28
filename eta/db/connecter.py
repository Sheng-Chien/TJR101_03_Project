from pymongo import MongoClient

# 建立連線
client = MongoClient('mongodb://tjr101g3:NewPassWord@35.221.213.83:27017/?authSource=admin')

# 選擇資料庫
db = client['test_clustor']

# 選擇集合（相當於SQL裡的表格）
collection = db['test_collection']

# 測試插入一筆資料
collection.insert_one({"name": "Alice", "age": 25})

# 測試查詢
result = collection.find_one({"name": "Alice"})
print(result)
