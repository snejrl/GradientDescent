import requests
import json
from urllib.parse import unquote
import time

# 1. 설정
authKey = unquote("Ot4%2FQ1tBWGAvCv8xHK6sUoo3YdCf7NnNnrDCoEgVS0F%2BSf5vvZeKgS2odW4kLm0J")
url = "https://opendata.koroad.or.kr/data/rest/stt"
output_file = "chungju_pm_data.json"

# 수집할 연도 범위
years = [str(y) for y in range(2010, 2025)]

all_data = []

print("--- 공주시 연도별 PM 사고 데이터 수집 시작 ---")

for year in years:
    params = {
        'authKey': authKey,
        'searchYearCd': year,
        'siDo': '1500',   # 충청남도
        'guGun': '1502',  # 공주시
        'type': 'json'
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get('resultCode') == '00':
            res_items = data.get('items', {})
            items = res_items.get('item', []) if isinstance(res_items, dict) else []
            
            # 단건 데이터일 경우 리스트로 변환
            if isinstance(items, dict):
                items = [items]

            # PM 사고 데이터만 필터링해서 추가
            found_pm = False
            for item in items:
                if item.get('acc_cl_nm') == '개인형이동수단(PM)사고':
                    all_data.append(item)
                    found_pm = True
            
            if found_pm:
                print(f"✅ {year}년: PM 사고 데이터 수집 완료")
            else:
                print(f"⚪ {year}년: PM 사고 데이터 없음")
        else:
            print(f"❌ {year}년: 에러 발생 ({data.get('resultMsg')})")

    except Exception as e:
        print(f"⚠️ {year}년: 요청 중 오류 발생 ({e})")
    
    # API 서버 부하를 줄이기 위한 짧은 휴식 (0.2초)
    time.sleep(0.2)

# 2. JSON 파일로 저장
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print("-" * 40)
print(f"총 {len(all_data)}건의 데이터를 '{output_file}'에 저장했습니다.")