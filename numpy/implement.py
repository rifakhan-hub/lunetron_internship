import numpy as np

a = np.array([5, 8, 7, 6, 3, 9])

print(a)
print(type(a))

b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(b)
print(type(b))

# array creation functions
print(np.zeros((2, 3)))         # 2x3 array of zeroes
print(np.ones((3, 3)))
print(np.full((3, 4), 5))       # 3x4 array filled with 5
print(np.eye(3))                # 3x3 identity matrix
print(np.arange(0, 10, 3))      # like python range but return an array
print(np.linspace(0,1, 5))      # 5 evenly space number between 0 and 1

print(np.random.rand(2, 2))         # 2x2 array of random floats between 0 and 1

# checking array properties

print(b.shape)
print(b.ndim)
print(a.size)
print(b.size)
print(b.dtype)