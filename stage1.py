import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1

# 1. 设置参数
D = 0.5e-3       # 圆孔半径，m
wavelength = 550e-9  # 波长，m
z = 1.0          # 观察距离，m
N = 2201          # 每个方向的采样点数

# 2. 生成观察平面坐标
x = np.linspace(-5e-3, 5e-3, N) # TODO：确定观察平面需要覆盖多大的范围
y = np.linspace(-5e-3, 5e-3, N) # TODO：确定观察平面需要覆盖多大的范围
X,Y= np.meshgrid(x,y)  # TODO：生成二维坐标网格

# 3. 计算每个位置的衍射强度
def calculate_intensity(x, y, D, wavelength, z):
    r = np.sqrt(x**2 + y**2)  # TODO：计算每个点到中心的距离
    theta = np.arctan2(r, z) # TODO：根据屏幕坐标计算观察角度
    u = np.pi * D * r / (wavelength * z)  # TODO：计算无量纲参数 u
    if np.any(u == 0):
        u[u==0] = 1e-10  # TODO：避免除以零，设置一个很小的值
    I = (2 * j1(u) / u)**2  # TODO：计算归一化强度
    return I


# 4. 计算强度并绘图
intensity = np.zeros((N, N))  # TODO：初始化强度矩阵
intensity = calculate_intensity(X, Y, D, wavelength, z)  # TODO：调用函数，生成二维强度矩阵
intensity[0, 0] = 1.0  # TODO：处理 u=0 的情况，避免除以零
#intensity = np.log10(intensity)  # TODO：对强度取对数，便于显示
plt.imshow(np.log10(intensity + 1e-6), 
           cmap='gray',
           extent = [-5, 5, -5, 5])  # TODO：设置显示范围
plt.colorbar(label='log10(Intensity)')
plt.xlabel('x (mm)')
plt.ylabel('y (mm)')
plt.show()
# 5. 理论验证
# TODO：计算理论第一暗环半径
r1 = 1.22 * wavelength * z / D
print("第一个暗环的半径：", r1, "m")
print("换算成毫米：", r1 * 1000, "mm")

row = np.argmin(np.abs(y))
line = intensity[row, :]
center = np.argmin(np.abs(x))

# 从中心右侧开始，寻找第一个局部最小值
for i in range(center + 1, len(x) - 1):
    if line[i] < line[i - 1] and line[i] < line[i + 1]:
        print("第一个暗点的 x 坐标：", x[i] * 1000, "mm")
        print("对应光强：", line[i])
        break
    
