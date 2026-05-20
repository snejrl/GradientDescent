import cv2
import mediapipe as mp
from pyfirmata import Arduino
import time

# =============================
# 1) 아두이노 연결
# =============================
board = Arduino('COM3')  # 포트 번호 확인 후 변경
led_pins = [2, 3, 4, 5, 6]

for pin in led_pins:
    board.digital[pin].mode = 1

# =============================
# 2) Mediapipe 손 설정
# =============================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.6,
                       min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# =============================
# 3) 손가락 개수 함수
# =============================
def count_fingers(hand_landmarks, handedness):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # 엄지
    thumb_tip = hand_landmarks.landmark[4].x
    thumb_ip = hand_landmarks.landmark[3].x
    if handedness == "Right":
        fingers.append(1 if thumb_tip < thumb_ip else 0)
    else:
        fingers.append(1 if thumb_tip > thumb_ip else 0)

    # 나머지 손가락
    compare_ids = {8:6, 12:10, 16:14, 20:18}
    for tip_id in [8,12,16,20]:
        tip_y = hand_landmarks.landmark[tip_id].y
        pip_y = hand_landmarks.landmark[compare_ids[tip_id]].y
        fingers.append(1 if tip_y < pip_y else 0)

    return sum(fingers)

# =============================
# 4) LED 제어
# =============================
def set_leds(count):
    count = max(0, min(5, count))
    for i, pin in enumerate(led_pins):
        board.digital[pin].write(1 if i < count else 0)

# =============================
# 5) 카메라 실행
# =============================
cap = cv2.VideoCapture(0)
prev_count = -1

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    finger_count = 0
    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        handedness = result.multi_handedness[0].classification[0].label
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
        finger_count = count_fingers(hand.landmark, handedness)
        cv2.putText(frame, f"Fingers: {finger_count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    else:
        cv2.putText(frame, "No hand", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    # LED 업데이트 (변경 시에만)
    if finger_count != prev_count:
        set_leds(finger_count)
        prev_count = finger_count

    cv2.imshow("Hand Tracking LED", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC 키로 종료
        break

cap.release()
board.exit()
cv2.destroyAllWindows()
