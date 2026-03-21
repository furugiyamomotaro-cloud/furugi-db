import os
from supabase import create_client

# GitHubに隠した合鍵を呼び出す
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# テスト用のデータ（あとで本物のスクレイピングデータに変えられます）
data = {
    "source_id": "test_001",
    "title": "テスト商品",
    "price": 1000,
    "brand": "ナイキ",
    "sold": False
}

# Supabaseの「商品」テーブルに保存
response = supabase.table("items").upsert(data).execute()
print("データを送信しました！")
