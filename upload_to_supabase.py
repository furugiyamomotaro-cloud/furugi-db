import os
import json
import glob
from supabase import create_client

# Supabase接続設定（GitHub Secretsから自動取得）
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# 設定
TABLE_NAME = "m5x5_v106_raw_intelligence"

def upload_json_files():
    # 1. リポジトリ内のすべてのmercari_..._data.jsonファイルを探す
    json_files = glob.glob("mercari_*_data.json")
    
    if not json_files:
        print("送信対象のJSONファイルが見つかりません。ファイルをアップロードしてください。")
        return

    for file_path in json_files:
        print(f"--- ファイル処理開始: {file_path} ---")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            total = len(data)
            print(f"読み込み成功: {total} 件のデータを送信します。")

            # 2. 500件ずつ小分けにして送信（API制限とエラー回避のため）
            for i in range(0, total, 500):
                batch = data[i:i+500]
                # upsertを使うことで、既存データがあれば更新、なければ挿入します
                supabase.table(TABLE_NAME).upsert(batch).execute()
                print(f"進捗: {i + len(batch)} / {total} 件完了")
                
        except Exception as e:
            print(f"ファイル {file_path} の処理中にエラーが発生しました: {e}")

if __name__ == "__main__":
    upload_json_files()
