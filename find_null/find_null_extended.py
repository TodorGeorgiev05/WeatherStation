# Find timestamps with NULL and 0 values, also entirely missing logs.
# This is for Timestamp, Temp, Humidity, Temp2, Humidity2, and Pressure.

import pandas as pd

csv_file_path = '/data/afterBME.csv'
df = pd.read_csv(csv_file_path)
print(df.head())
print(df.tail())

df['datetime'] = pd.to_datetime(df['datetime'], format="%m/%d/%Y %H:%M")

nan_rows = df[df.isna().any(axis=1)]
print(f"Rows with NaN: {len(nan_rows)}")
print(nan_rows)

zero_rows = df[(df.iloc[:, 1:] == 0).any(axis=1)]
print(f"Rows with zeros: {len(zero_rows)}")
print(zero_rows)

start = pd.Timestamp("2025-05-16 17:27")
end = pd.Timestamp("2025-05-30 17:18")
expected_range = pd.date_range(start=start, end=end, freq="3min")

missing = expected_range.difference(df['datetime'])

print(f"Total expected readings: {len(expected_range)}")
print(f"Actual readings: {len(df)}")
print(f"Missing readings: {len(missing)}")
print("Missing timestamps:")
print(missing)
