import pandas as pd

df = pd.read_csv("data.csv")

print(df)

# print(df.describe())
# print(df.info())
# print(df.shape)
# print(df.columns)
# print(df.dtypes)

# print("Duration")
# print(df["Duration"])
# print(df[df["Duration"]>55])
print(df.sort_values('Duration', ascending=True))

print(df.sort_values('Duration', ascending=False))
