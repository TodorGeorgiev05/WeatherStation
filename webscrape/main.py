# Websrape from wunderground. Everybody that have installed required libraries and choose a station.
# Please select the right link and on day, make {day} to work the cycle. If you need for one day, remove row-10 and row-152
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
for day in range(1, 31):
    url = f'https://www.wunderground.com/dashboard/pws/IHISAR6/table/2025-05-{day}/2025-05-{day}/daily'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    parsed_records = []

    try:
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'history-table.desktop-table'))
        )

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'lxml')

        history_table = soup.find('table', class_='history-table desktop-table')

        if history_table:
            headers = []
            header_row = history_table.find('thead').find('tr')
            if header_row:
                for th in header_row.find_all('th'):
                    headers.append(th.get_text(strip=True))
            
            # Name of the headers, in order, like in the site
            expected_headers = [
                "Time", "Temperature", "Dew Point", "Humidity", "Wind Direction", 
                "Wind Speed", "Gust", "Pressure", "Precip. Rate", "Precip. Accum.", 
                "UV", "Solar"
            ]
            
            if len(headers) != len(expected_headers):
                print(f"Warning: Scraped headers count ({len(headers)}) does not match expected headers ({len(expected_headers)})")
                headers = expected_headers 

            data_rows = history_table.find('tbody').find_all('tr')

            for row in data_rows:
                columns = row.find_all('td')
                # Extract raw text values
                raw_values = [col.get_text(strip=True) for col in columns]

                if not raw_values or len(raw_values) != len(headers):
                    print(f"Skipping row due to mismatch or empty: {raw_values}")
                    continue
                
                # Create a list for changing from imperial to metric
                processed_values = list(raw_values) 

                try:
                    # Time[0]
                    # No conversion needed, keep as string

                    # Temperature[1]
                    temp_str = processed_values[1].replace('°F', '').strip()
                    temp_f = float(temp_str)
                    processed_values[1] = round((temp_f - 32) * 5 / 9, 1)
                    
                    # Dew Point[2]
                    dew_str = processed_values[2].replace('°F', '').strip()
                    dew_f = float(dew_str)
                    processed_values[2] = round((dew_f - 32) * 5 / 9, 1)
                    
                    # Humidity[3]
                    humidity_str = processed_values[3].replace('°%', '').replace('%', '').strip()
                    processed_values[3] = int(humidity_str)
                    
                    # Wind Direction[4]
                    processed_values[4] = processed_values[4].strip()

                    # Wind Speed[5]
                    wind_speed_str = processed_values[5].replace('°mph', '').replace('mph', '').strip()
                    wind_mph = float(wind_speed_str)
                    processed_values[5] = round(wind_mph * 1.60934, 1)

                    # Gust[6]
                    gust_str = processed_values[6].replace('°mph', '').replace('mph', '').strip()
                    gust_mph = float(gust_str)
                    processed_values[6] = round(gust_mph * 1.60934, 1)
                    
                    # Pressure[7]
                    pressure_str = processed_values[7].replace('°in', '').replace('in', '').strip()
                    pressure_inhg = float(pressure_str)
                    processed_values[7] = round(pressure_inhg * 33.8639, 1)
                
                    # Precip. Rate[8]
                    precip_rate_str = processed_values[8].replace('°in/hr', '').replace('in/hr', '').replace('°in', '').replace('in', '').strip()
                    precip_rate_in = float(precip_rate_str)
                    processed_values[8] = round(precip_rate_in * 25.4, 2)
                    
                    # Precip. Accum[9]
                    precip_accum_str = processed_values[9].replace('°in', '').replace('in', '').strip()
                    precip_accum_in = float(precip_accum_str)
                    processed_values[9] = round(precip_accum_in * 25.4, 2)
                    

                    # UV[10]
                    uv_str = processed_values[10].strip()
                    processed_values[10] = int(uv_str)
                    

                    # Solar[11]
                    solar_str = processed_values[11].replace('w/m²', '').strip()
                    processed_values[11] = float(solar_str)
                    

                except ValueError as e:
                    print(f"Skipping row due to conversion error: {e}. Raw values: {raw_values}")
                    continue
                except IndexError as e:
                    print(f"Skipping row due to index error: {e}. Raw values: {raw_values}")
                    continue

                record_dict = dict(zip(headers, processed_values))
                parsed_records.append(record_dict)

        else:
            print("'history-table desktop-table' not found.")

    finally:
        driver.quit()

    if parsed_records:
        for i, record in enumerate(parsed_records[:5]):
            print(f"Record {i+1}: {record}")

        if len(parsed_records) > 5:
            print(f"... and {len(parsed_records) - 5} more records.")

        df = pd.DataFrame(parsed_records)
        print("\nPandas DataFrame - 5 rows")
        print(df.head())

    else:
        print("No data")
day +=1