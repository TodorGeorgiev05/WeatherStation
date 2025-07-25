import pandas as pd
import os

def clean_weather_data(input_csv_path, output_csv_path):

    if not os.path.exists(input_csv_path):
        print(f"Error: Input file not found at '{input_csv_path}'")
        return

    try:
        # Loading 4 headers: datetime, temperature, humidity, pressure ===
        df = pd.read_csv(input_csv_path, header=None, names=['datetime', 'temperature', 'humidity', 'pressure'])
        print(f"Initial rows loaded: {len(df)}")

        initial_rows_after_load = len(df)
        df = df[df['datetime'] != 'datetime']
        rows_removed_headers = initial_rows_after_load - len(df)
        if rows_removed_headers > 0:
            print(f"Removed {rows_removed_headers} rows identified as duplicate headers.")

        # Transforming into right dataframe types
        
        df['datetime'] = pd.to_datetime(df['datetime'], format="%m/%d/%Y %H:%M", errors='coerce')

        # Convert numeric columns, coercing errors to NaN
        df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
        df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')
        df['pressure'] = pd.to_numeric(df['pressure'], errors='coerce')
        print("Columns converted to correct data types.")

        # Drop rows where 'datetime' conversion failed 
        initial_rows_before_datetime_dropna = len(df)
        df.dropna(subset=['datetime'], inplace=True)
        rows_removed_invalid_datetime = initial_rows_before_datetime_dropna - len(df)
        if rows_removed_invalid_datetime > 0:
            print(f"Removed {rows_removed_invalid_datetime} rows with invalid datetime values.")

        # To keep from time duplicates
        initial_rows_before_deduplication = len(df)
        df.drop_duplicates(subset=['datetime'], keep='first', inplace=True)
        rows_removed_duplicates = initial_rows_before_deduplication - len(df)
        if rows_removed_duplicates > 0:
            print(f"Removed {rows_removed_duplicates} duplicate timestamp rows (keeping first occurrence).")

        nan_values_in_data = df[['temperature', 'humidity', 'pressure']].isna().sum().sum()
        if nan_values_in_data > 0:
            print(f"Warning: {nan_values_in_data} NaN values remain in numeric columns after cleaning.")
        else:
            print("No NaN values found in temperature, humidity, or pressure after cleaning.")

        zero_values_in_data = df[(df['temperature'] == 0) | (df['humidity'] == 0) | (df['pressure'] == 0)].shape[0]
        if zero_values_in_data > 0:
            print(f"Warning: {zero_values_in_data} rows contain zero values in temperature, humidity, or pressure.")
        else:
            print("No zero values found in temperature, humidity, or pressure after cleaning.")

        df.to_csv(output_csv_path, index=False, header=True) # index=False prevents writing DataFrame index as a column
        print(f"\nCleaned data saved to: {output_csv_path}")
        print(f"Final rows in cleaned file: {len(df)}")
        print("--- Data Cleaning Process Completed ---")

    except Exception as e:
        print(f"An error occurred during cleaning: {e}")

input_file = 'C:/Users/Asus/Desktop/Science/data/weather_2025-06-23_11-45-36.csv'
output_file = 'C:/Users/Asus/Desktop/Science/data/weather_cleaned_2025-06-23_11-45-36.csv' # New file name

if __name__ == "__main__":
    clean_weather_data(input_file, output_file)
