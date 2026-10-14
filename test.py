import numpy as np
x = np.array([-2, 0, 2])
y = np.array([-1, 1])
X, Y = np.meshgrid(x, y)
print(X.shape)
print(Y.shape)