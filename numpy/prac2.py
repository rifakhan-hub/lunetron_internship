import numpy as np 

a = np.array([10, 20, 30, 40, 50])

# 2 4x4 identity matrix
print(np.eye(4))

# 3x3 array of all 9s using
print(np.full((3, 3), 9))

# shape, ndim, and size.
b = np.array([[1, 2], [3, 4], [5, 6]])
print(b.shape)
print(b.ndim)
print(b.size)
print(b.dtype)