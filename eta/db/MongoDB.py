from pymongo import MongoClient

class MongoDB():

    def __init__(
            self,
            ip="35.221.213.83",
            user="tjr101g3",
            pw="NewPassWord",
            port=27017,
    ):
        url = f"mongodb://{user}:{pw}@{ip}:{port}/?authSource=admin"
        self.client = MongoClient(url)
        self.user = user
        self.ip = ip
    
    def __del__(self):
        self.client.close()


    def getDatabaseNames(self):
        return self.client.list_database_names()
    
    def show(self):
        print(f"IP2:{self.ip2}")
        print(f"IP:{self.ip}")
        print(f"USER:{self.user}")
        print()

    # 檢查資料庫存不存在
    def ifDBExist(self, database):
        db_list = self.client.list_database_names()
        if database in db_list:
            return True
        return False
    
