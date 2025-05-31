#ploting timestamp on x, values 0-100 on y, data is temp and humidity
import pandas as pd
import matplotlib.pyplot as plt
import io

def plot_temp_humidity(csv_data=None, csv_file_path=None):
    if csv_data is None and csv_file_path is None:
        print("Error: Either csv_data or csv_file_path must be provided.")
        return

    try:
        col_names = ['Timestamp', 'Temp', 'Humidity', 'Pressure', 'Unused', 'Humidity_Cleaned']
        df = pd.read_csv(csv_file_path if csv_file_path else io.StringIO(csv_data), names=col_names)

        df = df[~df['Timestamp'].astype(str).str.startswith('#')]

        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        df = df.dropna(subset=['Temp', 'Humidity'])

    except Exception as e:
        print(f"Error loading or processing data: {e}")
        return

    plt.figure(figsize=(11, 6))
    plt.plot(df['Timestamp'], df['Temp'], label='Temperature (°C)', color='red', marker='o', markersize=4)
    plt.plot(df['Timestamp'], df['Humidity'], label='Humidity (%)', color='blue', marker='x', markersize=4)

    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.title('Temperature and Humidity Over Time', fontsize=14)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    print("Preview of cleaned data:")
    print(df.tail())

    plt.show()

if __name__ == "__main__":
    csv_file_path = 'data/beforeBME.csv'
    plot_temp_humidity(csv_file_path=csv_file_path)
