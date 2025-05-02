import pymysql

# 建立連線
connection = pymysql.connect(
    host='104.199.214.113', # 主機位置
    user='test', # 使用者名稱
    port=3307, # 埠號
    password='PassWord_1', # 密碼
    charset='utf8mb4', # 避免中文亂碼
    # cursorclass=pymysql.cursors.DictCursor  # 讓結果以 dict 形式回傳（可選）
)

# 設定cursor
cursor = connection.cursor()

# 創建Database
sql = """
CREATE DATABASE IF NOT EXISTS
test_shema
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""
cursor.execute(sql)

# 指定schema
sql = """
USE test_shema;
"""
cursor.execute(sql)

# 插入一張表格
sql = """
CREATE TABLE IF NOT EXISTS sample_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    city VARCHAR(50),
    created_at DATETIME
);
"""
cursor.execute(sql)

# 插入測試資料
sql = """
INSERT INTO
sample_data (name, age, city, created_at)
VALUES
('Alice', 28, 'Taipei', NOW()),
('Bob', 35, 'Kaohsiung', NOW()),
('Charlie', 22, 'Tainan', NOW()),
('David', 40, 'Taichung', NOW()),
('Eva', 30, 'Hsinchu', NOW()),
('Frank', 27, 'Taipei', NOW()),
('Grace', 33, 'Taoyuan', NOW()),
('Hank', 29, 'Chiayi', NOW()),
('Irene', 31, 'Yilan', NOW()),
('Jack', 26, 'Keelung', NOW());
"""
cursor.execute(sql)
connection.commit() # 重要！pymysql沒有autucommit!

# 測試查詢
sql = """
select * from sample_data
"""
cursor.execute(sql)
results = cursor.fetchall()
print(results)

# 刪除
sql = """
drop table if exists sample_data
"""
# cursor.execute(sql)
connection.commit() # 重要！pymysql沒有autucommit!

sql = """
drop database if exists test_shema
"""
# cursor.execute(sql)
connection.commit() # 重要！pymysql沒有autucommit!


# 關閉連線
cursor.close()
connection.close()