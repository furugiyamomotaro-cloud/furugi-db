import os
import glob
import json
import pandas as pd
from supabase import create_client

# 1. カギの準備
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)
TABLE_NAME = "m5x5_v106_raw_intelligence"

def upload_json_files():
    # 2. 荷物をぜんぶ探す（".json" で終わるファイルなら全部見るよ！）
    json_files = glob.glob("*.json")
    
    # お仕事のジャマになるファイルはのぞくよ
    json_files = [f for f in json_files if f not in ['package.json', 'package-lock.json', 'config_local.json']]
    
    if not json_files:
        print("【しっぱい】荷物（JSONファイル）がひとつも見つからないよ！")
        return

    print(f"見つけた荷物: {json_files}")

    for file_path in json_files:
        print(f"--- {file_path} を運び始めるよ！ ---")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            df = pd.DataFrame(data)
            
            total = len(df)
            for i in range(0, total, 100):
                batch = df.iloc[i:i+100].to_dict(orient='records')
                supabase.table(TABLE_NAME).upsert(batch).execute()
                print(f"進捗: {min(i+100, total)} / {total} 件完了！")

        except Exception as e:
            print(f"エラーになっちゃった: {e}")

if __name__ == "__main__":
    upload_json_files()
