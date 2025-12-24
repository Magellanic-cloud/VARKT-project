import json
import matplotlib.pyplot as plt

def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

file1 = "data.json"
file2 = "ksp_data_v1_1.json"

data1 = load_data(file1)
data2 = load_data(file2)


fig, axes = plt.subplots(2, 1, figsize=(10, 10))

#1-ый график: скорость от времени
axes[0].plot(data1['time'], data1['speed'], label='Model', color='blue', linewidth=2)
axes[0].plot(data2['time'], data2['speed'], label='KSP', color='red', linewidth=2, linestyle='--')
axes[0].set_xlabel('Время (с)', fontsize=12)
axes[0].set_ylabel('Скорость (м/с)', fontsize=12)
axes[0].set_title('Зависимость скорости от времени', fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3)
axes[0].legend(loc='best')

#2-ой график: высота от времени
axes[1].plot(data1['time'], data1['altitude'], label='Model', color='green', linewidth=2)
axes[1].plot(data2['time'], data2['altitude'], label='KSP', color='orange', linewidth=2, linestyle='--')
axes[1].set_xlabel('Время (с)', fontsize=12)
axes[1].set_ylabel('Высота (м)', fontsize=12)
axes[1].set_title('Зависимость высоты от времени', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)
axes[1].legend(loc='best')

plt.tight_layout()
plt.show()

