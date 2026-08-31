import numpy as np

# 5x5 array of random integers between 1 and 100, find the max value in each row

a = np.random.randint(1, 100, (5, 5))
print(a)
for i in range(5):
    print(a[i, :].max())

# an array of the numbers 1–20, reshape it into a 4x5 matrix, and replace every even number with -1.

b = np.arange(1, 21)
print(b)
b = b.reshape(4, 5)
print(b)

b[b % 2 == 0] = -1
print(b)

# compute the discounted prices in one line using broadcasting

prices = np.array([100, 200, 150, 300]) 
discount = np.array([0.1])

print(prices - (prices*discount))