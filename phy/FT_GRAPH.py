import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 물리 상수 설정
m = 70          # 질량 (kg)
v = 5.56        # 속도 (20km/h)
delta_p = m * v # 총 충격량

# 2. 상황별 충돌 시간 정의
t_wall = 0.015     # 헬멧 착용 후 벽 충돌 (15ms)
t_sliding = 0.5    # 튕겨 나가서 미끄러짐 (1.5s 가정 - 100배 길어짐)

# 평균 충격력 계산
f_wall = delta_p / t_wall
f_sliding = delta_p / t_sliding

# 3. 데이터 생성 (가시성을 위해 sliding은 완만한 곡선으로 표현)
# 벽 충돌 데이터
t1 = np.linspace(0, t_wall, 100)
f1 = (delta_p / t_wall) * 2 * (1 - np.abs((t1 - t_wall/2) / (t_wall/2))) # 삼각형 모델

# 미끄러짐 데이터 (시간 축이 훨씬 길어서 로그 스케일이나 배율 조정 필요)
t2 = np.linspace(0, t_sliding, 100)
f2 = (delta_p / t_sliding) * 2 * (1 - np.abs((t2 - t_sliding/2) / (t_sliding/2)))

# 4. 그래프 시각화
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=False)

# [왼쪽] 정면 충돌 (순간적이고 강력한 힘)
ax1.plot(t1, f1, color='blue', linewidth=2, label='벽 충돌 (15ms)')
ax1.fill_between(t1, f1, color='blue', alpha=0.3)
ax1.set_title('Case 1: 정면 충돌 (헬멧 착용)', fontsize=13)
ax1.set_xlabel('시간 (s)')
ax1.set_ylabel('충격력 (N)')
ax1.annotate(f'Peak: {max(f1):,.0f}N', xy=(t_wall/2, max(f1)), xytext=(t_wall, max(f1)*0.8),
             arrowprops=dict(facecolor='black', shrink=0.05))

# [오른쪽] 미끄러짐 (시간 분산에 따른 힘의 약화)
ax2.plot(t2, f2, color='green', linewidth=2, label='미끄러짐 (1.5s)')
ax2.fill_between(t2, f2, color='green', alpha=0.3)
ax2.set_title('Case 2: 튕겨 나가 미끄러짐', fontsize=13)
ax2.set_xlabel('시간 (s)')
ax2.set_ylabel('충격력 (N)')
ax2.annotate(f'Peak: {max(f2):,.0f}N', xy=(t_sliding/2, max(f2)), xytext=(t_sliding*0.6, max(f1)*0.2),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.suptitle('충돌 메커니즘에 따른 충격력 분산 비교', fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()