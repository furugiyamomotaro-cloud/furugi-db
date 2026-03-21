import os
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

data = [
    {"name": "商品A", "price": 3000},
    {"name": "商品B", "price": 5000}
]

supabase.table("items").insert(data).execute()

print("OK")
