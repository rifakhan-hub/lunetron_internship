import numpy as np

a = np.arange(1, 17)
print(a.reshape(4, 4))

print(a.reshape(2, -1))

b = np.arange(10, 61, 10)
b = b.reshape(2, 3)
print(b)
print(b.T)

# broadcasting

a = np.array([[1,2,3],[4,5,6],[7,8,9]]) 
b = np.array([1,0,1])
print(a+b)

c = np.array([[1],[2],[3]]) 
print(c.shape)
d = np.array([10, 20, 30])
print(d.shape)
print(c+d)

