import numpy as np

a = np.array([1, 2, 3, 4, 5])
print(a*a)

a = np.array([2, 4, 6]) 
b = np.array([1, 2, 3])
print(a/b)

m = np.array([[1,2],[3,4],[5,6]])
print(f"sum of column: {m.sum(axis=0)}")
print(f"sum of rows: {m.sum(axis=1)} ")

c = np.array([4, 8, 6, 5, 3, 9])
print(f"mean: {c.mean()}")
print(f"standard deviation: {c.std()}")