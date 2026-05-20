import serial
import json
import time
import os
import matplotlib.pyplot as plt

# # -----------------------------
# # 설정
# # -----------------------------
# SERIAL_PORT = 'COM3'          # 시리얼 포트
# BAUD_RATE = 9600
# MEASURE_DURATION = 60         # 1분 측정
# FILTER_NAMES = ["hepa", "carbon", "gauze", "nano", "coffee", "kitchen"]
# JSON_FILE = "dust_data.json"

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# JSON_FILE = os.path.join(BASE_DIR, "dust_data.json")

# # 기존 JSON 파일 불러오기 (없으면 새로 생성)
# if os.path.exists(JSON_FILE):
#     with open(JSON_FILE, "r") as f:
#         data = json.load(f)
# else:
#     data = {name: [] for name in FILTER_NAMES}

# # 다음 저장할 필터 찾기
# for filter_name in FILTER_NAMES:
#     if len(data[filter_name]) == 0:
#         current_filter = filter_name
#         break
# else:
#     print("모든 필터 측정 완료!")
#     exit()

# print(f"Start measuring '{current_filter}' filter for {MEASURE_DURATION} seconds...")

# # -----------------------------
# # 시리얼 연결
# # -----------------------------
# ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
# time.sleep(2)  # 시리얼 초기화 대기

# # -----------------------------
# # 데이터 수집
# # -----------------------------
# count = 0
# while count < MEASURE_DURATION:
#     line_bytes = ser.readline()
#     line_str = line_bytes.decode('utf-8').strip()
#     if line_str.startswith("DUST,"):
#         value = float(line_str.split(",")[1])
#         data[current_filter].append(value)
#         count += 1
#         # 실시간 확인 출력
#         print(f"[{current_filter}] 측정 {count}/{MEASURE_DURATION}: {value} µg/m³")

# # -----------------------------
# # JSON 저장
# # -----------------------------
# with open(JSON_FILE, "w") as f:
#     json.dump(data, f, indent=4)

# print(f"\n'{current_filter}' filter measurement complete.")
# print(f"총 {len(data[current_filter])}개의 데이터가 '{JSON_FILE}'에 저장되었습니다.")
# print("현재 JSON 파일 내용 예시:")
# print(json.dumps({current_filter: data[current_filter]}, indent=4))


import json
import os
import matplotlib.pyplot as plt

# -----------------------------
# JSON 파일 경로 지정
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "dust_data.json")

# -----------------------------
# JSON 파일 불러오기
# -----------------------------
with open(JSON_FILE, "r") as f:
    data = json.load(f)

# -----------------------------
# 그래프 그리기
# -----------------------------
plt.figure(figsize=(12, 6))

# 색상 순서
import itertools
color_cycle = itertools.cycle(['red','green','blue','orange','purple','brown'])

for filter_name in data:
    values = data[filter_name]
    max_val = max(values)
    min_val = min(values)
    plt.plot(values, label=f"{filter_name} (max:{max_val}, min:{min_val})", color=next(color_cycle))

plt.title("PM2.5 Measurement by Filter")
plt.xlabel("Time (seconds)")
plt.ylabel("PM2.5 (µg/m³)")
plt.legend(loc='center')  # 범례 위치
plt.grid(True)
plt.tight_layout()
plt.show()
