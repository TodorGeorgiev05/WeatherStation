# Find timestamps with NULL and 0 values, also entirely missing logs.
# This is for Timestamp, Temperature, Humidity

import pandas as pd

csv_file_path = '/data/beforeBME.csv'
df = pd.read_csv(csv_file_path, header=None, names=['datetime', 'temperature', 'humidity'])
print(df.head())
print(df.tail())

nan_rows = df[df[['temperature', 'humidity']].isna().any(axis=1)]
print(f"\nRows with NaN values in 'temperature' or 'humidity': {len(nan_rows)}")
print(nan_rows)

zero_rows = df[(df['temperature'] == 0) | (df['humidity'] == 0)]
print(f"\nRows with 0 values in 'temperature' or 'humidity': {len(zero_rows)}")
print(zero_rows)

actual_timestamps = pd.to_datetime(df['datetime'], format="%m/%d/%Y %H:%M")

start = pd.Timestamp("2025-05-07 11:00")
end = pd.Timestamp("2025-05-16 15:20")
expected_range = pd.date_range(start=start, end=end, freq="3min")
missing = expected_range.difference(actual_timestamps)

print(f"\nTotal expected readings: {len(expected_range)}")
print(f"Actual readings: {len(actual_timestamps)}")
print(f"Missing readings: {len(missing)}")
print("Missing timestamps:")
print(missing)
