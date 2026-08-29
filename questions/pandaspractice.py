

import pandas as pd

# ==================================================================
# MODULE 1: MISSING VALUES 
# ==================================================================
print("#" * 70)
print("MODULE 1: MISSING VALUES")
print("#" * 70)

df1 = pd.DataFrame({
    'name': ['Alice', 'Bob', None, 'Dave', 'Eve'],
    'age': [25, None, 30, 22, None],
    'score': [88, 92, None, None, 75]
})
print("\nRaw:\n", df1)

print("\n-- Detect --")
print(df1.isnull())
print("\nNulls per column:\n", df1.isnull().sum())
print("\n% missing per column:\n", (df1.isnull().mean() * 100).round(1))

print("\n-- Drop --")
print("dropna() [any NaN row dropped]:\n", df1.dropna())
print("dropna(thresh=2) [keep rows with >=2 non-null]:\n", df1.dropna(thresh=2))

print("\n-- Fill --")
df1_fill = df1.copy()
df1_fill['age'] = df1_fill['age'].fillna(df1_fill['age'].mean())
df1_fill['score'] = df1_fill['score'].fillna(df1_fill['score'].median())
df1_fill['name'] = df1_fill['name'].fillna('Unknown')
print(df1_fill)

print("\n-- Interpolate (good for time series / ordered numeric data) --")
df1_interp = df1.copy()
df1_interp['age'] = df1_interp['age'].interpolate()
print(df1_interp[['age']])

# UNDERSTANDING:
# - Use dropna() only when missing rows are a small % and not informative.
# - Use fillna(mean/median) for numeric columns; median is safer with outliers.
# - Use fillna('Unknown'/'Missing') for categorical/text columns — never drop silently.
# - interpolate() is best for ordered/sequential data (time series, sensor readings).


# ==================================================================
# MODULE 2: DUPLICATE HANDLING  
# ==================================================================
print("\n" + "#" * 70)
print("MODULE 2: DUPLICATE HANDLING")
print("#" * 70)

df2 = pd.DataFrame({
    'order_id': [1, 2, 2, 3, 4],
    'customer': ['Alice', 'Bob', 'Bob', 'Alice', 'Charlie'],
    'amount': [100, 200, 200, 100, 300]
})
print("\nRaw:\n", df2)

print("\nFull-row duplicates:\n", df2.duplicated())
print("\nDrop full-row duplicates:\n", df2.drop_duplicates())
print("\nDuplicate by subset (customer+amount), keep last:\n",
      df2.drop_duplicates(subset=['customer', 'amount'], keep='last'))

# UNDERSTANDING:
# - duplicated() flags rows identical to an EARLIER row (first occurrence = False).
# - Always prefer subset=[...] with real business keys over full-row matching —
#   two rows can differ by an irrelevant column (like a timestamp) and still be
#   logical duplicates.
# - keep='first' (default) / 'last' / False (drop ALL copies including original).


# ==================================================================
# MODULE 3: TEXT / STRING CLEANING  
# ==================================================================
print("\n" + "#" * 70)
print("MODULE 3: TEXT / STRING CLEANING")
print("#" * 70)

df3 = pd.DataFrame({
    'name': [' alice smith ', 'BOB JONES', 'Charlie   Lee', ' dave ']
})
print("\nRaw:\n", df3)

df3['clean_name'] = (
    df3['name']
    .str.strip()                       # remove leading/trailing spaces
    .str.replace(r'\s+', ' ', regex=True)  # collapse multiple spaces
    .str.title()                       # proper case
)
print("\nCleaned:\n", df3)

df3['initial'] = df3['clean_name'].str[0]
df3['word_count'] = df3['clean_name'].str.split().str.len()
print("\nDerived features:\n", df3)

# UNDERSTANDING:
# - .str accessor works element-wise on a Series, like Python string methods
#   but vectorized (fast, no manual loop needed).
# - Always .strip() before comparing/deduplicating text — hidden whitespace
#   is a very common silent bug.
# - regex=True enables pattern-based replace within str.replace().


# ==================================================================
# MODULE 4: CATEGORICAL CLEANING  
# ==================================================================
print("\n" + "#" * 70)
print("MODULE 4: CATEGORICAL CLEANING")
print("#" * 70)

df4 = pd.DataFrame({
    'city': ['NY', 'new york', 'New York', 'ny', 'LA', 'Los Angeles', 'la']
})
print("\nRaw:\n", df4)

mapping = {
    'ny': 'New York', 'new york': 'New York',
    'la': 'Los Angeles', 'los angeles': 'Los Angeles'
}
df4['city_clean'] = df4['city'].str.lower().map(mapping)
print("\nStandardized via mapping:\n", df4)

df4['city_clean'] = df4['city_clean'].astype('category')
print("\nDtype after conversion:\n", df4.dtypes)
print("\nCategories:", df4['city_clean'].cat.categories.tolist())

# One-hot encoding
print("\nOne-hot encoded:\n", pd.get_dummies(df4['city_clean'], prefix='city'))

# UNDERSTANDING:
# - Free-text categorical fields ("NY" vs "new york" vs "New York") are a top
#   real-world data quality issue — always normalize case before mapping.
# - astype('category') saves memory and speeds up groupby for low-cardinality columns.
# - get_dummies() is the standard pandas one-hot encoder for ML-ready features.


# ==================================================================
# MODULE 5: DATA TYPE CONVERSION  
# ==================================================================
print("\n" + "#" * 70)
print("MODULE 5: DATA TYPE CONVERSION")
print("#" * 70)

df5 = pd.DataFrame({
    'id': ['1', '2', '3'],
    'price': ['19.99', '25.50', 'unknown'],
    'is_active': ['True', 'False', 'True'],
    'joined': ['2023-01-01', '2023-06-15', '2024-01-10']
})
print("\nRaw dtypes:\n", df5.dtypes)

df5['id'] = df5['id'].astype(int)
df5['price'] = pd.to_numeric(df5['price'], errors='coerce')   # 'unknown' -> NaN
df5['is_active'] = df5['is_active'].map({'True': True, 'False': False})
df5['joined'] = pd.to_datetime(df5['joined'])

print("\nConverted:\n", df5)
print("\nNew dtypes:\n", df5.dtypes)

# UNDERSTANDING:
# - astype() fails hard on bad values; pd.to_numeric/to_datetime with
#   errors='coerce' fails softly (turns bad values into NaN/NaT) — much safer
#   for real-world messy data.
# - Correct dtypes matter: string "19.99" can't be summed, but float 19.99 can.


# ==================================================================
# MODULE 6: NUMERICAL CLEANING  
# ==================================================================
print("\n" + "#" * 70)
print("MODULE 6: NUMERICAL CLEANING")
print("#" * 70)

df6 = pd.DataFrame({
    'price': ['$100', '$250.50', '$75', '$-10', '$0']
})
print("\nRaw:\n", df6)

df6['price_clean'] = (
    df6['price']
    .str.replace('$', '', regex=False)
    .astype(float)
)
print("\nAfter removing currency symbol:\n", df6)

# Fix invalid negative prices
df6['price_clean'] = df6['price_clean'].where(df6['price_clean'] >= 0)
print("\nInvalid negatives -> NaN:\n", df6)

# Round to 2 decimals
df6['price_clean'] = df6['price_clean'].round(2)
print("\nRounded:\n", df6)

# UNDERSTANDING:
# - Numeric-looking text (currency, percentages, units like "kg"/"cm") must be
#   stripped of symbols before converting to float.
# - .where(condition) keeps values where True, replaces with NaN where False —
#   useful for flagging impossible values (negative price, age > 150, etc).


# ==================================================================
# MODULE 7: DATE & TIME CLEANING  
# ==================================================================
print("\n" + "#" * 70)
print("MODULE 7: DATE & TIME CLEANING")
print("#" * 70)

df7 = pd.DataFrame({
    'event_date': ['2024-01-05', '01/15/2024', '2024-13-40', '2024-03-01']
})
print("\nRaw:\n", df7)

df7['event_date_clean'] = pd.to_datetime(df7['event_date'], errors='coerce')
print("\nParsed (invalid -> NaT):\n", df7)

df7['year'] = df7['event_date_clean'].dt.year
df7['month'] = df7['event_date_clean'].dt.month_name()
df7['weekday'] = df7['event_date_clean'].dt.day_name()
df7['is_weekend'] = df7['event_date_clean'].dt.dayofweek >= 5
print("\nExtracted features:\n", df7)

# UNDERSTANDING:
# - pd.to_datetime auto-detects most common formats, but mixed formats in one
#   column (as shown here) can still cause misparses — always eyeball results.
# - errors='coerce' is essential; without it, ONE bad date crashes the whole column.
# - The .dt accessor unlocks year/month/weekday/quarter etc. once dtype is datetime.


# ==================================================================
# MODULE 8: OUTLIER DETECTION 
# ==================================================================
print("\n" + "#" * 70)
print("MODULE 8: OUTLIER DETECTION")
print("#" * 70)

df8 = pd.DataFrame({'salary': [45000, 48000, 51000, 47000, 300000, 46000, 49000]})
print("\nRaw:\n", df8)

q1 = df8['salary'].quantile(0.25)
q3 = df8['salary'].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
print(f"\nIQR bounds: [{lower}, {upper}]")

outliers = df8[(df8['salary'] < lower) | (df8['salary'] > upper)]
print("\nOutliers:\n", outliers)

df8['salary_capped'] = df8['salary'].clip(lower=lower, upper=upper)
print("\nCapped (winsorized):\n", df8)

# UNDERSTANDING:
# - IQR method: anything beyond 1.5x the interquartile range is a statistical
#   outlier — a standard, robust, non-parametric rule of thumb.
# - clip() caps extreme values instead of deleting the row — keeps the sample
#   size while limiting the outlier's influence on averages/models.


# ==================================================================
# MODULE 9: CONDITIONAL CLEANING  
# ==================================================================
print("\n" + "#" * 70)
print("MODULE 9: CONDITIONAL CLEANING")
print("#" * 70)

df9 = pd.DataFrame({
    'age': [15, 25, -5, 200, 40],
    'income': [0, 50000, 30000, 45000, -1000]
})
print("\nRaw:\n", df9)

# Replace impossible ages with NaN
df9['age'] = df9['age'].where((df9['age'] >= 0) & (df9['age'] <= 120))
# Replace negative income with 0
df9['income'] = df9['income'].mask(df9['income'] < 0, 0)
print("\nCleaned:\n", df9)

# np.select equivalent using pandas-only nested conditions
def age_group(age):
    if pd.isna(age):
        return 'Unknown'
    elif age < 18:
        return 'Minor'
    elif age < 60:
        return 'Adult'
    else:
        return 'Senior'

df9['age_group'] = df9['age'].apply(age_group)
print("\nWith derived group:\n", df9)

# UNDERSTANDING:
# - .where(cond) keeps values where cond is True, else NaN (default).
# - .mask(cond) is the OPPOSITE: replaces values where cond is TRUE.
# - For multi-branch logic, .apply() with a custom function is clear and
#   pandas-only (no numpy.select needed).


# ==================================================================
# MODULE 10: REGEX CLEANING  
# ==================================================================
print("\n" + "#" * 70)
print("MODULE 10: REGEX CLEANING")
print("#" * 70)

df10 = pd.DataFrame({
    'contact': ['Call 123-456-7890', 'Email: bob@test.com', 'Phone: (987) 654-3210', 'no info']
})
print("\nRaw:\n", df10)

df10['phone'] = df10['contact'].str.extract(r'(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})')
df10['email'] = df10['contact'].str.extract(r'([\w\.-]+@[\w\.-]+\.\w+)')
df10['digits_only'] = df10['contact'].str.replace(r'\D', '', regex=True)
print("\nExtracted:\n", df10)

df10['has_valid_email'] = df10['contact'].str.contains(r'@\w+\.\w+', regex=True, na=False)
print("\nValidation flag:\n", df10[['contact', 'has_valid_email']])

# UNDERSTANDING:
# - str.extract() pulls the first regex match into a new column — great for
#   parsing structured info buried in free text.
# - str.contains() returns a boolean mask — perfect for validation flags/filters.
# - Always pass na=False in contains() so missing text doesn't raise/propagate NaN
#   into a boolean filter.


# ==================================================================
# MODULE 11: GROUP-BASED CLEANING  
# ==================================================================
print("\n" + "#" * 70)
print("MODULE 11: GROUP-BASED CLEANING")
print("#" * 70)

df11 = pd.DataFrame({
    'department': ['Sales', 'Sales', 'Sales', 'IT', 'IT', 'IT'],
    'salary': [50000, None, 55000, 70000, 72000, None]
})
print("\nRaw:\n", df11)

# Fill missing salary with THAT department's average (not the global average)
df11['salary_filled'] = df11.groupby('department')['salary'].transform(
    lambda x: x.fillna(x.mean())
)
print("\nGroup-wise fill:\n", df11)

# Flag rows above their department's average
df11['dept_avg'] = df11.groupby('department')['salary_filled'].transform('mean')
df11['above_avg'] = df11['salary_filled'] > df11['dept_avg']
print("\nWith comparison flag:\n", df11)

# UNDERSTANDING:
# - groupby().transform() returns a Series the SAME LENGTH as the original
#   DataFrame (unlike agg(), which collapses rows) — so it can be assigned
#   straight back as a new column.
# - This is far more accurate than a single global fillna(mean()), since
#   different groups (departments, categories, regions) often have very
#   different typical values.


# ==================================================================
# MODULE 12: DATA VALIDATION  
# ==================================================================
print("\n" + "#" * 70)
print("MODULE 12: DATA VALIDATION")
print("#" * 70)

df12 = pd.DataFrame({
    'email': ['a@test.com', 'bad-email', 'b@test.org', 'also_bad'],
    'age': [25, 150, -5, 40],
    'id': [1, 2, 2, 4]
})
print("\nRaw:\n", df12)

df12['valid_email'] = df12['email'].str.match(r'^[\w\.-]+@[\w\.-]+\.\w+$')
df12['valid_age'] = df12['age'].between(0, 120)
df12['is_duplicate_id'] = df12.duplicated(subset=['id'], keep=False)

print("\nValidation flags:\n", df12)

# Assert-style hard checks (raises if violated — useful in pipelines/tests)
try:
    assert df12['valid_age'].all(), "Found rows with invalid age!"
except AssertionError as e:
    print(f"\nValidation failed: {e}")

# Summary validation report
report = pd.DataFrame({
    'check': ['valid_email', 'valid_age', 'no_duplicate_id'],
    'pass_rate_%': [
        df12['valid_email'].mean() * 100,
        df12['valid_age'].mean() * 100,
        (~df12['is_duplicate_id']).mean() * 100
    ]
})
print("\nValidation report:\n", report)

# UNDERSTANDING:
# - str.match() anchors regex at the start (^) — good for full-field format checks.
# - .between() is a clean, readable range check (inclusive by default).
# - assert stops a pipeline hard when a critical rule breaks — better than
#   silently shipping bad data downstream.


# ==================================================================
# MODULE 13: MERGE + CLEANING  
# ==================================================================
print("\n" + "#" * 70)
print("MODULE 13: MERGE + CLEANING")
print("#" * 70)

customers = pd.DataFrame({
    'cust_id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'Dave']
})
orders = pd.DataFrame({
    'cust_id': [1, 2, 2, 5],
    'amount': [100, 200, 150, 300]
})
print("\nCustomers:\n", customers)
print("\nOrders:\n", orders)

merged = pd.merge(orders, customers, on='cust_id', how='left', indicator=True)
print("\nLeft merge with indicator (spot unmatched rows):\n", merged)

unmatched = merged[merged['_merge'] == 'left_only']
print("\nOrders with no matching customer (data quality issue!):\n", unmatched)

merged['name'] = merged['name'].fillna('Unknown Customer')
merged = merged.drop(columns=['_merge'])
print("\nCleaned merged result:\n", merged)

# UNDERSTANDING:
# - indicator=True adds a '_merge' column showing 'left_only'/'right_only'/'both' —
#   the fastest way to catch orphaned foreign keys after a join.
# - how='left' keeps ALL rows from the primary table even without a match —
#   essential when you need to know what's MISSING, not just what matched.
# - Post-merge, always check for and fill/flag unmatched rows — a silent
#   inner join can quietly drop real data.


# ==================================================================
# MODULE 14: DATA QUALITY REPORTS  
# ==================================================================
print("\n" + "#" * 70)
print("MODULE 14: DATA QUALITY REPORTS")
print("#" * 70)

df14 = pd.DataFrame({
    'id': [1, 2, 3, 3, 5],
    'name': ['Alice', 'Bob', None, None, 'Eve'],
    'age': [25, -5, 30, 30, 200],
    'email': ['a@x.com', 'bad', 'c@x.com', 'c@x.com', 'e@x.com']
})
print("\nRaw:\n", df14)

def data_quality_report(df):
    report = pd.DataFrame({
        'dtype': df.dtypes,
        'missing_count': df.isnull().sum(),
        'missing_%': (df.isnull().mean() * 100).round(1),
        'unique_values': df.nunique(),
        'duplicate_rows': df.duplicated().sum()
    })
    return report

print("\nData quality report:\n", data_quality_report(df14))

# UNDERSTANDING:
# - A reusable quality-report function is standard practice before any cleaning
#   begins — it tells you WHERE to focus effort (which columns, how bad).
# - Building this once and calling it on every new dataset saves huge time
#   in real projects.


# ==================================================================
# MODULE 15: COMPLETE CLEANING PIPELINE  
# ==================================================================
print("\n" + "#" * 70)
print("MODULE 15: COMPLETE CLEANING PIPELINE")
print("#" * 70)

raw = pd.DataFrame({
    'Order ID': [1, 2, 2, 3, 4, None],
    ' Customer ': [' alice ', 'BOB', 'bob', 'Charlie', ' dave', 'eve'],
    'Order Date': ['2024-01-05', '2024-02-10', '2024-02-10', 'bad_date', '2024-03-01', '2024-03-15'],
    'Amount': ['$100', '$250.5', '$250.5', 'N/A', '$75', '$9999'],
    'Category': ['electronics', 'ELECTRONICS', 'Electronics', 'clothing', 'clothing', 'clothing']
})
print("\nRaw input:\n", raw)

def clean_pipeline(df):
    df = df.copy()

    # 1. Column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # 2. Text cleaning (BEFORE dedup)
    df['customer'] = df['customer'].str.strip().str.title()
    df['category'] = df['category'].str.strip().str.title()

    # 3. Deduplicate on business key
    df = df.drop_duplicates(subset=['customer', 'order_date'])

    # 4. Type conversion
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['amount'] = pd.to_numeric(
        df['amount'].str.replace('$', '', regex=False), errors='coerce'
    )

    # 5. Missing value handling (group-based)
    df['amount'] = df.groupby('category')['amount'].transform(
        lambda x: x.fillna(x.median())
    )
    df = df.dropna(subset=['order_id'])

    # 6. Outlier capping
    q1, q3 = df['amount'].quantile(0.25), df['amount'].quantile(0.75)
    iqr = q3 - q1
    df['amount'] = df['amount'].clip(q1 - 1.5 * iqr, q3 + 1.5 * iqr)

    # 7. Validation flag
    df['valid_date'] = df['order_date'].notna()

    # 8. Final reset
    df = df.reset_index(drop=True)
    return df

cleaned = clean_pipeline(raw)
print("\nFinal cleaned output:\n", cleaned)
print("\nInfo:\n")
print(cleaned.info())

# UNDERSTANDING — PIPELINE ORDER MATTERS:
# names -> text clean -> dedup -> types -> missing values -> outliers -> validate -> reset_index
# Cleaning text BEFORE dedup catches "BOB" vs "bob" as the same duplicate.
# Converting types BEFORE filling missing values ensures fillna/median works on
# actual numbers, not strings. Outlier handling comes AFTER missing-value fill
# so capping isn't skewed by NaNs. Validation flags come last, once data is stable.
