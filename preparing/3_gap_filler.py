import pandas as pd
import os # To handle file paths and check for existence

def fill_missing_weather_data(input_cleaned_csv_path, output_filled_csv_path):

    if not os.path.exists(input_cleaned_csv_path):
        print(f"Error: Input cleaned file not found at '{input_cleaned_csv_path}'")
        return

    try:
        # 1. Load the cleaned CSV file
        # We expect the cleaned file to have a header row(from 2.cleaner) now, so we don't use header=None
        df = pd.read_csv(input_cleaned_csv_path)
        print(f"Initial rows loaded from cleaned file: {len(df)}")

        # Ensure 'datetime' is in datetime format
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        # Drop any rows where datetime conversion might still fail 
        df.dropna(subset=['datetime'], inplace=True)

        # Set 'datetime' as the DataFrame index for time-series operations like reindexing and interpolation
        df.set_index('datetime', inplace=True)

        df.sort_index(inplace=True)
        print("Datetime column set as index and sorted.")

        # 2. Find the missing timestamps
        start_time = df.index.min()
        end_time = df.index.max()
        # Generate a complete expected date range at 3-minute intervals
        expected_range = pd.date_range(start=start_time, end=end_time, freq="3min")

        # Reindex the DataFrame to this complete range.
        df_reindexed = df.reindex(expected_range)

        # Count how many NaNs were introduced
        initial_missing_count = df_reindexed['temperature'].isna().sum()
        if initial_missing_count > 0:
            print(f"Identified {initial_missing_count} missing timestamps that will be filled.")
        else:
            print("No missing timestamps found in the expected range. Data is already complete.")
            df_reindexed.to_csv(output_filled_csv_path, index=True, header=True) #
            print(f"\nData already complete. Saved to: {output_filled_csv_path}")
            print("--- Missing Data Filling Process Completed ---")
            return

        # Fill missing values using linear interpolation 
        # Linear interpolation fills NaN values based on the values before and after them.
        # This effectively calculates the average of the two nearest valid data points
        df_filled = df_reindexed.interpolate(method='time', limit_direction='both')
        # 'method='time'' is suitable for time series data.
        # limit_direction='both' ensures interpolation works even if NaNs are at the start/end

        # Check if all NaNs are filled should be for internal NaNs with 'time' method
        final_missing_count = df_filled['temperature'].isna().sum()
        if final_missing_count == 0:
            print("All missing values successfully filled using linear interpolation.")
        else:
            print(f"Warning: {final_missing_count} NaN values remain after interpolation.")

        df_filled.reset_index(inplace=True)
        df_filled.rename(columns={'index': 'datetime'}, inplace=True) 

        df_filled.to_csv(output_filled_csv_path, index=False, header=True) 
        print(f"\nFilled data saved to: {output_filled_csv_path}")
        print(f"Final rows in filled file: {len(df_filled)}")

    except Exception as e:
        print(f"An error occurred during filling: {e}")

input_file_for_filling = 'C:/Users/Asus/Desktop/Science/data/weather_cleaned_2025-06-23_11-45-36.csv'
output_file_after_filling = 'C:/Users/Asus/Desktop/Science/data/weather_filled_2025-06-23_11-45-36.csv'

if __name__ == "__main__":
    fill_missing_weather_data(input_file_for_filling, output_file_after_filling)
