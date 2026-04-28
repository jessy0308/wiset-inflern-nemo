import os
import requests
import pandas as pd
import sqlite3

def main():
    # 저장할 디렉토리 생성
    os.makedirs('data', exist_ok=True)
    os.makedirs('src', exist_ok=True)

    url = "https://www.nemoapp.kr/api/store/search-list"
    params = {
        "Subway": "222",
        "Radius": "1000",
        "CompletedOnly": "false",
        "NELat": "37.52414970837205",
        "NELng": "127.05773954072409",
        "SWLat": "37.46772194890557",
        "SWLng": "126.97422665668671",
        "Zoom": "15",
        "SortBy": "29",
        "PageIndex": "0"
    }

    headers = {
        "referer": "https://www.nemoapp.kr/store",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        print("전체 데이터를 수집하는 중...")
        all_items = []
        page_index = 0
        
        while True:
            params["PageIndex"] = str(page_index)
            print(f"PageIndex {page_index} 수집 중...")
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # HTTP 에러가 발생하면 예외 처리
            data = response.json()
            
            items = data.get("items", [])
            if not items:
                print("더 이상 데이터가 없습니다. 수집을 종료합니다.")
                break
                
            all_items.extend(items)
            page_index += 1

        print(f"총 {len(all_items)}개의 아이템을 가져왔습니다.")

        if all_items:
            df = pd.DataFrame(all_items)
            
            # 리스트나 딕셔너리 같은 복합 데이터 구조를 문자열로 변환 (SQLite 저장 오류 방지)
            for col in df.columns:
                if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
                    df[col] = df[col].astype(str)
            
            # SQLite 데이터베이스에 연결하고 데이터 저장
            db_path = os.path.join('data', 'nemo_stores.db')
            conn = sqlite3.connect(db_path)
            df.to_sql('stores', conn, if_exists='replace', index=False)
            conn.close()
            print(f"데이터베이스 저장 완료: {db_path} (stores 테이블)")
        else:
            print("데이터의 items 리스트가 비어 있습니다.")
            
    except Exception as e:
        print(f"데이터 수집 및 저장 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
