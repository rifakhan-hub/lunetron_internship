import numpy as np

a = np.array([5, 10, 15, 20, 25, 30])
print(a[0:4])  # get elements at positions 1 through 4

b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(b.shape)
print(b[:, 1])      # extract the middle column

c = np.array([2, 7, 3, 9, 4, 11])
print(c[c > 5])     # the values greater than 5

d = np.array([1, -2, 3, -4, 5])
d[d<0] = 0      # Replace all negative numbers with 0
print(d)
