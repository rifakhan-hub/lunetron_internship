import pandas as pd

df = pd.read_csv("Map-Scraper_20260826123513.csv")

new_df = df[df["Emails"].str.contains("@gmail.com", na=False)]
# Keep the entire row only if its Emails field contains a Gmail address

new_df["Emails"] = new_df["Emails"].str.extract(r'([\w.-]+@gmail\.com)')
print(new_df["Emails"])

new_df = new_df[["Name", "Phone", "Emails"]]

new_df = new_df.drop_duplicates()

print(new_df)

new_df.to_csv("cleaned_data.csv", index=False)