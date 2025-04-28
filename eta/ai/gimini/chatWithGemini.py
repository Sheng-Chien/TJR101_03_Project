import google.auth
import google.auth.exceptions
from vertexai.preview.generative_models import GenerativeModel
import google.generativeai as genai

from google.oauth2 import service_account
from google.cloud import aiplatform
import json


class ChatWithGemini():
    # 設定地區
    _location = "us-central1"
    # 價格
    _price = {
        "gemini-2.0-flash":{
            "input": 0.1 /1000,
            "output": 0.4 /1000,
        }
    }

    def __init__(self, key_path="",
                max_tonkens=500,
                temperature=0.5,
                top_p=0.9,
                top_k=40,
        ):
        self.setKey(key_path)
        self.model = "gemini-2.0-flash"
        self.region = "us-central1"
        self.max_tonkens = max_tonkens
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k

    # 放棄使用ADC登入功能，但先保留
    def ifADC(self, text=False):
        # 檢查ADC狀態
        try:
            # 嘗試由 application Default Credentials 取得憑證
            auth_info = google.auth.default()
            if text: 
                print("✅ ADC 認證成功")
            self.project_id = auth_info[-1]
            return True
        except google.auth.exceptions.DefaultCredentialsError:
            if text:
                print("❌ ADC 認證失敗")    

    # 04/28 讀取模型清單不適用於金鑰模式
    # def ifKey(self, text=False):
    #     # 嘗試載入金鑰設定
    #     try:
    #         aiplatform.Model.list()
    #         if text:
    #             print("✅ 金鑰載入成功")
    #         return True
    #     except:
    #         if text:
    #             print("❌ 金鑰載入失敗")
    #         return False


    # 指定本地端的json金鑰
    def setKey(self, key_path=""):
        try:
            credentials = service_account.Credentials.from_service_account_file(key_path)
            with open(key_path, mode="r") as f:
                project_id = json.load(f)["project_id"]
            self.project_id = project_id
            aiplatform.init(
                project=project_id,
                location=self._location,
                credentials=credentials,
                )
            print("金鑰設定成功")
            return True

        except:
            return False


    def chat(self, prompt):
        # 初始化 Vertex AI Python 函式庫
        aiplatform.init(project=self.project_id, location=self.region)
        # 設定模型參數
        model = GenerativeModel(
            model_name=self.model,
            generation_config={
                "temperature": self.temperature,
                "max_output_tokens": self.max_tonkens,
                "top_p": self.top_p,
                "top_k": self.top_k,
            }
        )
        response = model.generate_content(prompt)
        return response.to_dict()
    
    # 功能尚未啟用
    def pricing(self, prompt):
        # model = genai.
        credentials, project_id = google.auth.default()
        aiplatform.init(project=project_id, location=self._location, credentials=credentials)

        models = aiplatform.Model.list()
        print(models)
        genai
    
    def getAuthInfo(self):
        print(self.project_id)
