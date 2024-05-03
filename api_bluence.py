import requests
import pandas as pd
from datetime import timedelta


def fetch_ts_bluence_data(signal_addresses, f_desde, f_hasta):
    """
    Fetch timeseries data from APM Bluence API based on this parameters:

    Parameters:
        signal_addresses (str): List of signal_addresses, has to be the same time frecuency (10M, 1H, etc)
        from_ts (str): The start date in YYYY-MM-DD HH:MM format.
        to_ts (str): The end date in YYYY-MM-DD HH:MM format.

    Returns:
        pd.DataFrame: DataFrame containing the fetched data.
    """
    # Convert from_ts and to_ts to the desired format
    from_ts = pd.to_datetime(from_ts).strftime("%Y-%m-%dT%H:%M:%SZ")
    to_ts = pd.to_datetime(to_ts).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Convert list of signal addresses to comma-separated string
    signal_addresses_str = ",".join(signal_addresses)

    url = f"https://centralpuerto.bluence.com/rest/datasets/timeseries.json?asset_addresses=&asset_element_addresses=&signal_addresses={signal_addresses_str}&from_ts={from_ts}&to_ts={to_ts}"
    headers = {'Authorization': '369011a13e533b61cf04d3e7ce239b31-Cpu'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        json_response = response.json()
        
        df = pd.DataFrame()
        
        # Extract and concatenate timeseries data for each signal address
        for signal_address in signal_addresses:
            # Extract the timeseries data for the current signal address
            timeseries_data = json_response["timeseries"][signal_address]
            
            # Convert to DataFrame
            temp_df = pd.DataFrame.from_dict(timeseries_data, orient="index")
            
             # Convert the index to datetime with UTC timezone
            temp_df.index = pd.to_datetime(temp_df.index, utc=True)
            
            # Convert timezone to 'America/Argentina/Buenos_Aires' (UTC-3)
            temp_df.index = temp_df.index.tz_convert('America/Argentina/Buenos_Aires')
            
            # Convert the index to datetime and format it
            temp_df.index = pd.to_datetime(temp_df.index).strftime("%Y-%m-%d %H:%M")
            
            # Rename the column to the signal address
            temp_df.rename(columns={"v": signal_address}, inplace=True)
            
            # Convert to numeric signal address and round 2
            temp_df[signal_address] = pd.to_numeric(temp_df[signal_address]).round(2)  
            
            # Concatenate the DataFrame to the result DataFrame
            df = pd.concat([df, temp_df], axis=1)
        
        # Rename the index to "FechaHora"
        df.index.name = "FechaHora"
        
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

