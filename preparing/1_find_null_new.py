import pandas as pd

csv_file_path = 'C:/Users/Asus/Desktop/Science/data/weather_2025-06-23_11-45-36.csv'

# Loading 4 headers: datetime, temperature, humidity, pressure ===
df = pd.read_csv(csv_file_path, header=None, names=['datetime', 'temperature', 'humidity', 'pressure'])

df = df[df['datetime'] != 'datetime']

# Transforming into right dataframe types
df['datetime'] = pd.to_datetime(df['datetime'], format="%m/%d/%Y %H:%M", errors='coerce')
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')
df['pressure'] = pd.to_numeric(df['pressure'], errors='coerce')

# Remove rows with incorrect values
df.dropna(subset=['datetime'], inplace=True)

# To keep from time duplicates
df.drop_duplicates(subset=['datetime'], keep='first', inplace=True)

print(df.head())
print(df.tail()) 

# Check for NaNs ir 0
nan_rows = df[df[['temperature', 'humidity']].isna().any(axis=1)]
print(f"\nRows with NaN values in 'temperature' or 'humidity': {len(nan_rows)}")
print(nan_rows)

zero_rows = df[(df['temperature'] == 0) | (df['humidity'] == 0)]
print(f"\nRows with 0 values in 'temperature' or 'humidity': {len(zero_rows)}")
print(zero_rows)

start = df['datetime'].min()
end = df['datetime'].max()

# Using set() automatically handles the duplicate datetime in the actual_timestamps set
actual_timestamps = set(df['datetime'])

# Generate the full expected range
expected_range = pd.date_range(start=start, end=end, freq="3min")

# Find the difference
missing = expected_range.difference(actual_timestamps)

# This loop is useful for showing the actual timestamps in order (after converting set to sorted list)
print("\n--- Iterating through Actual Timestamps (sorted) ---")
for i, timestamp in enumerate(sorted(list(actual_timestamps))):
    # Print a few to show it works, or all if you want to see them all
    if i < 5 or i > len(actual_timestamps) - 5: # Print first 5 and last 5 
        print(f"Index {i}: {timestamp}")
    elif i == 5:
        print("...") 

# This part correctly identifies and prints the missing timestamps
missing_timestamps_list = list(missing) # Convert to list for easier handling if needed
if missing_timestamps_list:
    print("\n--- Missing Timestamps Details ---")
    for i, ts in enumerate(missing_timestamps_list):
        expected_index = expected_range.get_loc(ts)
        print(f"Missing Timestamp: {ts} (Expected Integer Index in full range: {expected_index})")
else:
    print("\nNo missing timestamps found.")

print(f"\nTotal expected readings: {len(expected_range)}")
print(f"Actual unique readings: {len(actual_timestamps)}")
print(f"Missing readings: {len(missing)}")
print("Missing timestamps:")
print(missing)
