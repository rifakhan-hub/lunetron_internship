import pandas as pd

df = pd.read_csv("data.csv")

# print(df)

# print(df.describe())
# print(df.info())
# print(df.shape)
# print(df.columns)
# print(df.dtypes)

# print("Duration")
# print(df["Duration"])
# print(df[df["Duration"]>55])
# print(df.sort_values('Duration', ascending=True))

# print(df.sort_values('Duration', ascending=False))

# basic filtering 

print(df[(df["Duration"]>50) & (df["Pulse"]>110)])
print(df[(df["Calories"]>400)&(df["Maxpulse"]>140)])

# filtering + selecting column

data = df[df["Calories"]>400]
print(data.loc[:,["Date", "Calories"]])

print(df.loc[df["Pulse"]>110, ["Date", "Pulse", "Maxpulse"]])

print(df.loc[(df["Pulse"]>110)& (df["Calories"]>400), ["Date", "Pulse", "Calories"]])

# isin() - selcting multiple values
print(df[ df["Pulse"].isin([103, 110, 117])])

print(df[ (df["Duration"].isin([45, 60])) & (df["Calories"]>400)] )