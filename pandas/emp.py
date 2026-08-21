import pandas as pd

print(pd.__version__)

data = {
    "id" : [1, 2, 3, 4],
    "names" : ["raj", "aman", "riya", "oshi"],
    "class" : [5, 8, 10, 7],
    "subject" : ["maths", "physics", "maths", "chemistry"],
    "age": [20, 21, 22, 20]
}

df = pd.DataFrame(data)
print(df)

print(df.iloc[3])
print(df.shape)
print(df.dtypes)
print(df.columns)
print(df["names"])
print(df.iloc[0])
# result = df[df["class"]>8]
# result = df[df["age"]==22]

result = df[(df["age"]>20) & (df["age"]<22)]
print(result)

print(df.describe())
