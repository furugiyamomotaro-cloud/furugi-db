from supabase import create_client
import os

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise Exception("SUPABASE_URL または SUPABASE_KEY が未設定")

supabase = create_client(url, key)

data = {
    "name": "test",
    "price": 1000
}

res = supabase.table("items").insert(data).execute()

print(res)
