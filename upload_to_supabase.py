import os
import glob
import json
import pandas as pd
from supabase import create_client

# 1. Supabase（金庫）へのカギ
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)
TABLE_NAME = "m5x5_v106_raw_intelligence"

def upload_json_files():
    # 2. 荷物（JSONファイル）をぜんぶ探す
    # フォルダの中にある「mercari_」で始まるファイルを全部見つけるよ！
    json_files = glob.glob("mercari_*.json")
    
    if not json_files:
        print("【しっぱい】荷物（JSONファイル）がひとつも見つからないよ！")
        return

    for file_path in json_files:
        print(f"--- {file_path} を運び始めるよ！ ---")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 3. データをきれいに並べなおす（お掃除）
            df = pd.DataFrame(data)
            
            # 4. 少しずつ（100個ずつ）金庫に入れる
            total = len(df)
            for i in range(0, total, 100):
                batch = df.iloc[i:i+100].to_dict(orient='records')
                supabase.table(TABLE_NAME).upsert(batch).execute()
                print(f"進捗: {min(i+100, total)} / {total} 件完了！")

        except Exception as e:
            print(f"エラーになっちゃった: {e}")

if __name__ == "__main__":
    upload_json_files()
