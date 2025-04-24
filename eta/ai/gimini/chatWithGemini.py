import google.auth
import google.auth.exceptions
import google.generativeai as genai
from vertexai.preview.generative_models import GenerativeModel

from google.oauth2 import service_account
from pathlib import Path
from google.cloud import aiplatform
import json


class chatWithGemini():
    def __init__(self, key_path=""):
        self.setKey(key_path)

    def ifAuth(self, text=False):
        try:
            # 嘗試由 application Default Credentials 取得憑證
            auth_info = google.auth.default()
            if text: 
                print("✅ 認證成功")
                print(f"目前專案：{auth_info[-1]}")
            return True
        except google.auth.exceptions.DefaultCredentialsError:
            if text:
                print("❌ 認證失敗，請確認已登入GCP或匯入金鑰")
            return False

    # 指定本地端的json金鑰
    def setKey(self, key_path):
        try:
            credentials = service_account.Credentials.from_service_account_file(key_path)
            aiplatform.init(credentials=credentials)
        except:
            pass
        aiplatform.init(
        # project="794747612771",       # ← 請改成你的 GCP Project ID
        project="tibameproject",       # ← 請改成你的 GCP Project ID
        # location="asia-east1",            # Gemini 支援地區
        location="us-central1",            # Gemini 支援地區
        # credentials=credentials,
        )
       

    # ADC問題尚未解決，只判定KEY
    def ifAuthed(self):
        try:
            models = aiplatform.Model.list()
            print("成功列出模型。憑證可能已正確設定。")
            # 可以進一步檢查 models 是否為一個列表
            # print(models)
        except Exception as e:
            print(f"列出模型失敗: {e}")
            print("憑證可能設定不正確，或者你的服務帳戶沒有列出模型的權限。")

        try:
            datasets = aiplatform.Dataset.list()
            print("成功列出資料集。憑證可能已正確設定。")
            # 可以進一步檢查 datasets 是否為一個列表
            # print(datasets)
        except Exception as e:
            print(f"列出資料集失敗: {e}")
            print("憑證可能設定不正確，或者你的服務帳戶沒有列出資料集的權限。")
    
    def chat(self):
        aiplatform.init(
        # project="794747612771",       # ← 請改成你的 GCP Project ID
        project="tibameproject",       # ← 請改成你的 GCP Project ID
        # location="asia-east1",            # Gemini 支援地區
        location="us-central1",            # Gemini 支援地區
        # credentials=credentials,
        )
        model = GenerativeModel("gemini-2.0-flash")
        prompt = "請用100左右字說個故事。"
        response = model.generate_content(prompt)
        # ✅ 組合 JSON 資料
        response_data = {
            "prompt": prompt,
            "response": response.text
        }

        # ✅ 儲存為 JSON 檔案
        with open("response.json", "w", encoding="utf-8") as f:
            json.dump(response_data, f, ensure_ascii=False, indent=2)

        print("✅ 回應已儲存至 response.json")

# # 使用GCP ADC登入
# # 指定您的服務帳戶匯出金鑰檔案的路徑
# KEY_FILE_PATH = "C:/Users/Tibame/Documents/Tibame_Project/Gemini/tibameproject-2506260bd94b.json"  # 替換為您的金鑰檔案路徑

# # 建立憑證物件
# # credentials = service_account.Credentials.from_service_account_file(KEY_FILE_PATH)
# # 不指定就會直指ADC所建立的憑證

# aiplatform.init(
#     # project="794747612771",       # ← 請改成你的 GCP Project ID
#     project="tibameproject",       # ← 請改成你的 GCP Project ID
#     # location="asia-east1",            # Gemini 支援地區
#     location="us-central1",            # Gemini 支援地區
#     # credentials=credentials,
# )

# # 用金鑰設定API
# # 設定 API 金鑰
# genai.configure(api_key=API_KEY)
# # 初始化 Gemini-Pro 模型
# model = genai.GenerativeModel("gemini-2.0-flash")

# # 取得回應
# response = model.generate_content(prompt)

# # 初始化 Gemini-Pro 模型
# model = genai.GenerativeModel("gemini-2.0-flash")
        
        


def main():
    key_path = Path(__file__).parent / ".data/tibameproject-2506260bd94b.json"
    ask_gemini = chatWithGemini(key_path=key_path)
    ask_gemini.ifAuth(text=True)
    ask_gemini.ifAuthed()
    # ask_gemini.chat()

if __name__ == "__main__":
    main()