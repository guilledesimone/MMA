import requests
import pandas as pd
from datetime import timedelta


def smec_data(id_smec, f_desde, f_hasta):
    """
    Busca los datos desde la API SMEC basado en los parametros.

    Parameters:
        id_smec (str): The idSmec value.
        f_desde (str): The start date in YYYY-MM-DD format.
        f_hasta (str): The end date in YYYY-MM-DD format.

    Returns:
        pd.DataFrame: DataFrame containing the fetched data.
    """
    # Construct the URL with parameters
    url = f"https://smecscpsa.apis-raixen.com/?idSmec={id_smec}&fDesde={f_desde}&fHasta={f_hasta}"

    headers = {
        'APIKEY': 'QdXldSFGD6rKVv4LIXx4eqNjtFKROCjIk2xNVMM8',
        'USEREMAIL': 'ap-synergy@centralpuerto.com'
    }

    response = requests.get(url, headers=headers) #, verify=False)
    data = response.json()

    # Extracting channel descriptions
    channels_data = data[0]['canales']
    channel_descriptions = {channel['id']: channel['descripcion'] for channel in channels_data}

    # Extracting measurements
    measurements_data = data[0]['mediciones']

    # Creating DataFrame
    df = pd.DataFrame(measurements_data)

    # Renaming columns using channel descriptions
    df.rename(columns=channel_descriptions, inplace=True)

    # Remplazo el 24:00 por 00:00 y le sumo 1 dia para poder sumarizar correctamente los registros de la hora 00:00
    df['momento_hora']=df['momento_hora'].replace({'24:00': '00:00'})
    
    df['FechaHora'] = pd.to_datetime(df['momento_fecha'] + ' ' + df['momento_hora']) + \
    pd.to_timedelta(df['momento_hora'].eq('00:00').astype(int), unit='D')
    
    
    return df

def calcular_energia_lcas(f_desde, f_hasta):
    
    id_smecs = ["LCASM61P", "LCASM62P", "LCA2M61P"]
    
    # Collect data for each id_smec into separate DataFrames
    data_frames = {}
    for id_smec in id_smecs:
        data_frames[id_smec] = smec_data(id_smec, f_desde, f_hasta)

    # Initialize a DataFrame to store the total Energia Activa Recibida by FechaHora
    total_energia_recibida_df = pd.DataFrame()

    # Calculate the total Energia Activa Recibida for each id_smec and add it to the DataFrame
    for id_smec, df in data_frames.items():
        total_energia_recibida_df[id_smec] = pd.to_numeric(df.groupby('FechaHora')['Energia Activa Recibida'].sum(), errors='coerce')

    # Calculate the desired operations
    total_energia_recibida_df['total'] = (total_energia_recibida_df["LCASM61P"] + total_energia_recibida_df["LCASM62P"] - total_energia_recibida_df["LCA2M61P"])/1000

    # Agrego 45 minutos a 'FechaHora' para poder sumarizar los 4 valores de la hora
    total_energia_recibida_df.index = total_energia_recibida_df.index + timedelta(minutes=45)

    # Resample to hourly frequency and calculate the sum for each column
    total_energia_recibida_df_h = total_energia_recibida_df.resample('h').sum().round(2)

    total_energia_recibida_df_h.reset_index(inplace=True)

    # Rename the column "total" to "EnergiaSMEC"
    total_energia_recibida_df_h.rename(columns={'total': 'EnergiaSMEC'}, inplace=True)

    return total_energia_recibida_df_h
