import pandas as pd
import io

# 1. Simulate a client's messy CSV (Missing values, duplicates, bad dates)
messy_data = """id,name,score,date
1,Alice,85,2023/01/05
2,Bob,,2023/02/10
3,Alice,85,2023/01/05
4,Charlie,92,2023-03-12
5,Dave,78,
"""

# 2. Load it into pandas
df = pd.read_csv(io.StringIO(messy_data))

print("--- RAW MESSY DATA ---")
print(df)

# 3. CLEAN IT (The 3 Laws of Pandas)
# Law 1: Kill exact duplicate rows
df = df.drop_duplicates()

# Law 2: Fill missing numbers with the average
df['score'] = df['score'].fillna(df['score'].mean())

# Law 3: Force all dates into one standard format
df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')

print("\n--- CLEANED DATA ---")
print(df)

# 4. Save to a clean CSV
df.to_csv("data/clean_output.csv", index=False)
print("\nSaved to data/clean_output.csv")
