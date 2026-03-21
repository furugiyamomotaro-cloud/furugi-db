import os
import random
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

TOTAL = 170000
BATCH_SIZE = 500

for start in range(0, TOTAL, BATCH_SIZE):
    data = []

    for i in range(start, start + BATCH_SIZE):
        data.append({
            "name": f"商品{i}",
            "price": random.randint(1000, 5000)
        })

    supabase.table("items").upsert(data).execute()

    print(f"{start} 件〜 {start + BATCH_SIZE} 件 完了")
