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