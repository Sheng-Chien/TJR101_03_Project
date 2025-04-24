import google.auth
from google.auth.exceptions import DefaultCredentialsError

try:
    credentials, project_id = google.auth.default()
    print("✅ 已成功載入 ADC 憑證")
    print("🔐 帳號：", credentials.service_account_email if hasattr(credentials, "service_account_email") else "非服務帳號")
    print("📁 專案 ID：", project_id)
except DefaultCredentialsError as e:
    print("❌ ADC 憑證無法使用：", e)
