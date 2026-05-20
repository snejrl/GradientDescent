import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**2 - 4*x + 4

def df(x):
    return 2*x - 4

learning_rate = 0.1  
epochs = 50          
tolerance = 1e-4    

current_x = -2.0

history = {
    'x': [],         
    'gradient': [], 
    'loss': []       
}

print("=== 경사하강법 최적화 시작 ===")
for i in range(epochs):
    current_loss = f(current_x)
    current_gradient = df(current_x)
    
    history['x'].append(current_x)
    history['gradient'].append(current_gradient)
    history['loss'].append(current_loss)
    
    if i % 5 == 0:
        print(f"Step {i:2d} | x위치: {current_x:.4f} | 기울기: {current_gradient:.4f} | 오차: {current_loss:.4f}")
    
    if abs(current_gradient) < tolerance:
        print(f"\n조기 종료: {i}번째 반복에서 최적점 수렴 완료 (기울기가 0에 근접)")
        break
        
    current_x = current_x - (learning_rate * current_gradient)

print(f"\n최종 탐색된 최적의 x값: {current_x:.4f}")


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

x_range = np.linspace(-3, 7, 1000)
ax1.plot(x_range, f(x_range), label='Loss Function: f(x)', color='blue', alpha=0.6)
ax1.scatter(history['x'], history['loss'], color='red', zorder=5, label='Search Path')
ax1.plot(history['x'], history['loss'], color='red', linestyle='--', alpha=0.5)

ax1.set_title('Gradient Descent Path')
ax1.set_xlabel('x')
ax1.set_ylabel('Loss')
ax1.legend()
ax1.grid(True)

ax2.plot(range(len(history['gradient'])), history['gradient'], marker='o', color='green', label='Gradient Value')
ax2.axhline(0, color='black', linestyle='--', alpha=0.5, label='Target (Gradient = 0)')
ax2.set_title('Gradient Convergence over Iterations')
ax2.set_xlabel('Iteration Step')
ax2.set_ylabel('Gradient')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()