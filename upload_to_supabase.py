import os, glob, json, pandas as pd
from supabase import create_client

# 1. 接続設定
url, key = os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)
TABLE = "m5x5_v106_raw_intelligence"

def vol48_run():
    # 2. DBのカラム構成（正解の棚）を自動取得
    try:
        res = supabase.table(TABLE).select("*").limit(1).execute()
        db_cols = list(res.data[0].keys()) if res.data else []
        print(f"--- [vol.48] DB同期完了: {len(db_cols)}項目 ---")
    except Exception as e:
        print(f"❌ DB接続エラー: {e}"); return

    # 3. JSONファイルの読み込みと強制整形
    target_files = glob.glob("mercari_*_data.json")
    for f_path in target_files:
        print(f"📦 処理中: {f_path}")
        try:
            with open(f_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            # 各行の項目数が違っても強制的にDBの形に合わせる（エラー回避の肝）
            df = pd.DataFrame(raw_data)
            for col in db_cols:
                if col not in df.columns: df[col] = None
            
            # DBに存在するカラムのみ抽出し、順序を揃える
            sync_data = df[db_cols].to_dict(orient='records')
            
            # 4. バッチ送信（100件ずつ慎重に送信）
            total = len(sync_data)
            for i in range(0, total, 100):
                batch = sync_data[i:i+100]
                supabase.table(TABLE).upsert(batch).execute()
                print(f"   🚀 送信済み: {min(i+100, total)} / {total}")
                
        except Exception as e:
            print(f"❌ エラー({f_path}): {e}")

if __name__ == "__main__": vol48_run()
