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

# indexing and slicing

a[0]   # first element
a[-1]  # last element
a[1:4]  # from index 1 to 3
a[: 3]  # first 3 elements
a[::2]  # every second element

b[0, 0]     # 1 row 0, column 0
b[1, :]     # entire row 1 
b[:, 2]     # entire column 2
b[0:2, 0:2]     # top left 2x2 block

# conditional

a[a>2]      # elements greater than 2
a[a%3 == 0]     # elements divisible by 3
a[a > 3] = 1    # replace all elements greater than 3 with 1


# array operations/ vectorization

a = np.array([1, 2, 3]) 
b = np.array([4, 5, 6])
print([(a+b), (a-b), (a*b), (a/b)])  # element wise operation
print(a**2)

np.sqrt(b)      # square root of each element 
np.exp(a)       # e^x for each element 
np.log(a)       # natural log of each element 
np.abs(-a)      # absolute value

a = np.array([[1, 2, 3], [4, 5, 6]])

print(a.sum())         # sum of all elements
print(a.sum(axis=0))   # sum down each column
print(a.sum(axis=1))   # sum across each row

print(a.mean())
print(a.max())
print(a.min())
print(a.std())      # standard deviation
print(a.argmax())   # index of max value


# Reshaping Arrays

x = np.arange(12)   # an array of 12 element

print(x.reshape(3,4))
print(x.reshape(2, -1))     # -1 means "figure this dimension out automatically"

print(x.flatten())          # collapse back to 1D
print(x.T)                  # transpose (flip rows/columns) for 2D arrays

# Useful Extras

print(np.concatenate([a+b]))
print(np.vstack([a, b]))
# print(np.hstack([a, b]))
print(np.sort(a))
print(np.unique(a))

