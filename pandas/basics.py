# pandas_env/Scripts/activate

import pandas as pd 

print(pd.__version__)

data={
    "Name": ["Raj", "aman", "Riya", "Yaashi"],
    "Age": [21, 22, 20, 21],
    "City": ["bhopal", "Mumbai", "Pune", "Delhi"],
    "Salary": [10000, 15000, 9000, 12000]
}

df = pd.DataFrame(data)

print(df)
print(df.iloc[0])
print(df.iloc[0:2])

result = df[df["Salary"] > 10000]
print(result)

print(df.shape)
print(df.dtypes)


print(df.head(1))
print(df.tail(1))

print(df.describe)