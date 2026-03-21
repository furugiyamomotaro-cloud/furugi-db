from supabase import create_client
import os
import random

# 環境変数
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise Exception("SUPABASE_URL または SUPABASE_KEY が未設定")

# 接続
supabase = create_client(url, key)

# データ作成（5件）
data = []

for i in range(5):
    data.append({
        "name": f"商品{i}_{random.randint(1,1000)}",
        "price": random.randint(500, 5000)
    })

# INSERT
res = supabase.table("items").insert(data).execute()

# ログ
print("=== INSERT結果 ===")
print(res)
