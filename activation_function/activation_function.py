import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# ----------------------------------------------------
# 1. 비선형 나선형 (Spiral) 데이터셋 생성 함수
# ----------------------------------------------------
def create_spiral_data(points, classes):
    X = np.zeros((points * classes, 2))
    y = np.zeros(points * classes, dtype='uint8')
    
    for j in range(classes):
        ix = range(points * j, points * (j + 1))
        r = np.linspace(0.0, 1, points)
        t = np.linspace(j * 4, (j + 1) * 4, points) + np.random.randn(points) * 0.2
        
        X[ix] = np.c_[r * np.sin(t*2.5), r * np.cos(t*2.5)]
        y[ix] = j
        
    return X, y

# 데이터 생성
X, y = create_spiral_data(points=100, classes=2)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# ----------------------------------------------------
# 2. 비교할 활성화 함수 리스트
# ----------------------------------------------------
activation_functions = ['linear', 'sigmoid', 'tanh', 'relu']
results = {}

# 함수별로 모델을 생성, 학습 및 평가
for activation in activation_functions:
    print(f"\n--- 학습 시작: {activation.upper()} 활성화 함수 ---")

    # 2-Layer Neural Network 모델 정의 (은닉층 2개)
    model = Sequential([
        Dense(4, activation=activation, input_shape=(2,)), 
        Dense(4, activation=activation),
        Dense(1, activation='sigmoid') 
    ])

    # 모델 컴파일
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    
    # 모델 학습 (500 에포크)
    history = model.fit(X_train, y_train, 
                        epochs=500, 
                        validation_data=(X_val, y_val), 
                        verbose=0)
    
    # 최종 검증 성능 평가
    loss, accuracy = model.evaluate(X_val, y_val, verbose=0)
    
    results[activation] = {
        'loss': loss,
        'accuracy': accuracy,
        'history': history
    }
    
    print(f"함수: {activation.upper()} | 최종 검증 손실(Loss): {loss:.4f} | 최종 정확도(Accuracy): {accuracy:.4f}")

# ----------------------------------------------------
# 3. 결과 시각화
# ----------------------------------------------------
plt.figure(figsize=(15, 5))

# 손실(Loss) 변화 추이 그래프
plt.subplot(1, 2, 1)
for activation, res in results.items():
    plt.plot(res['history'].history['val_loss'], label=f'{activation.upper()} Loss')
plt.title('Validation Loss Comparison (500 Epochs)')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

# 정확도(Accuracy) 변화 추이 그래프
plt.subplot(1, 2, 2)
for activation, res in results.items():
    plt.plot(res['history'].history['val_accuracy'], label=f'{activation.upper()} Accuracy')
plt.title('Validation Accuracy Comparison (500 Epochs)')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')
plt.grid(True)

plt.tight_layout()
plt.show()