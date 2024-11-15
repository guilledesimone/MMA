##Funciones de limpieza


## Función remover_valores_repetidos: remueme los valores que estan repetidos para una columna del dataframe n o mas veces.
## Parametros:
## df: Dataframe con datos de series temporales
## date_column: Columna de fecha de la serie temporal
## column_to_check: Columna en la que se verifican repetidos
## min_consecutive: Cantidad minimo de valores repetidos
## verbose: Imprime el valor repetido, cantidad de veces y rango de fecha en el que se repite 

def remover_valores_repetidos(df, date_column, column_to_check, min_consecutive, verbose):
    
    from datetime import timedelta #tuve que agregarlo por que no toma la definida a nivel global
    
    rep_count = 1
    rep_tot = 0
    start_date = None
    end_date = None
    date_ranges = []
  
    for index, row in df.iterrows():
        if index == 0:
            prev_value = row[column_to_check]
            start_date = row[date_column]           
        else:
            if row[column_to_check] == prev_value:
                rep_count += 1
                if rep_count == min_consecutive:
                    start_date = row[date_column] - timedelta(hours=min_consecutive-1) 
                #Es para cuando los valores repetidos estan en los ultimos registros
                if rep_count >= min_consecutive and index == len(df) - 1:
                    end_date = row[date_column] - timedelta(hours=1)
                    date_ranges.append((prev_value,rep_count,start_date, end_date))
                    rep_tot = rep_tot + rep_count
            else:
                if rep_count >= min_consecutive:
                    end_date = row[date_column] - timedelta(hours=1)
                    date_ranges.append((prev_value,rep_count,start_date, end_date))
                    rep_tot = rep_tot + rep_count
                    rep_count = 1
                    start_date = row[date_column]         
                rep_count = 1
        
        prev_value = row[column_to_check]

    if verbose=='y':
        print(f"Se removieron {rep_tot} registros repetidos")
        for prev_value, rep_count, start, end in date_ranges:
            print(f"Remueve el valor {prev_value} repetido {rep_count} veces: {start} - {end}")
    else:
        print(f"Se removieron {rep_tot} registros repetidos")
    
    
    #remueve los valores repetidos
    for prev_value, rep_count, start, end in date_ranges:
        df = df[~((df[date_column] >= start) & (df[date_column] <= end))]
    
    
    return df


###############################################################################

## Función rango_fechas_repe_exc: devuelve los rangos de fechas en los que existen valores repetidos para una columna del dataframe n o mas veces.
## Parametros:
## df: Dataframe con datos de series temporales
## date_column: Columna de fecha de la serie temporal
## column_to_check: Columna en la que se verifican repetidos
## min_consecutive: Cantidad minimo de valores repetidos
## exclude_val: Valor queda excluido en la verificación de repetidos 

def rango_fechas_repe_exc(df, date_column, column_to_check, min_consecutive, exclude_val):
    
    from datetime import timedelta #tuve que agregarlo por que no toma la definida a nivel global
    
    rep_count = 1
    start_date = None
    end_date = None
    date_ranges = []
  
    for index, row in df[df[column_to_check]!=exclude_val].iterrows():
        if index == 0:
            prev_value = row[column_to_check]
            start_date = row[date_column]           
        else:
            if row[column_to_check] == prev_value:
                rep_count += 1
                if rep_count == min_consecutive:
                    start_date = row[date_column] - timedelta(hours=min_consecutive-1) 
                #Es para cuando los valores repetidos estan en los ultimos registros
                if rep_count >= min_consecutive and index == len(df) - 1:
                    end_date = row[date_column] - timedelta(hours=1)
                    date_ranges.append((prev_value,rep_count,start_date, end_date))
                    rep_tot = rep_tot + rep_count      
            
            else:
                if rep_count >= min_consecutive:
                    end_date = row[date_column] - timedelta(hours=1)
                    date_ranges.append((prev_value,rep_count,start_date, end_date))
                    rep_count = 1
                    start_date = row[date_column]         
                rep_count = 1
        
        prev_value = row[column_to_check]

    for prev_value, rep_count, start, end in date_ranges:
        print(f"Rango de fechas para valor {prev_value} repetido {rep_count} veces: {start} - {end}")

    
    return date_ranges

#########################################################################################


## Función rango_fechas_repe: devuelve los rangos de fechas en los que existen valores repetidos para una columna del dataframe n o mas veces.
## Parametros:
## df: Dataframe con datos de series temporales
## date_column: Columna de fecha de la serie temporal
## column_to_check: Columna en la que se verifican repetidos
## min_consecutive: Cantidad minimo de valores repetidos
## verbose: Imprime el valor repetido, cantidad de veces y rango de fecha en el que se repite 


def rango_fechas_repe(df, date_column, column_to_check, min_consecutive, verbose):
    
    from datetime import timedelta #tuve que agregarlo por que no toma la definida a nivel global
    
    rep_count = 1
    rep_tot = 0
    start_date = None
    end_date = None
    date_ranges = []
  
    for index, row in df.iterrows():
        if index == 0:
            prev_value = row[column_to_check]
            start_date = row[date_column]           
        else:
            if row[column_to_check] == prev_value:
                rep_count += 1
                if rep_count == min_consecutive:
                    start_date = row[date_column] - timedelta(hours=min_consecutive-1) 
                #Es para cuando los valores repetidos estan en los ultimos registros
                if rep_count >= min_consecutive and index == len(df) - 1:
                    end_date = row[date_column] - timedelta(hours=1)
                    date_ranges.append((prev_value,rep_count,start_date, end_date))
                    rep_tot = rep_tot + rep_count  
            else:
                if rep_count >= min_consecutive:
                    end_date = row[date_column] - timedelta(hours=1)
                    date_ranges.append((prev_value,rep_count,start_date, end_date))
                    rep_tot = rep_tot + rep_count
                    rep_count = 1
                    start_date = row[date_column]         
                rep_count = 1
        
        prev_value = row[column_to_check]

    if verbose=='y':
        print(f"Existen {rep_tot} registros repetidos")
        for prev_value, rep_count, start, end in date_ranges:
            print(f"Valor {prev_value} repetido {rep_count} veces en las fechas: {start} - {end}")
         
    else:
        print(f"Existen {rep_tot} registros repetidos")

    
    return date_ranges

##########################################################################################################

#Función weighted_circular_mean: Caluculo del promedio ponderado circular
## Parametros:
## values: valor circlular a promediar
## weights: variable que pondera en el calculo del promerdio


def weighted_circular_mean(values, weights):
    
    import numpy as np # no la toma de la definición global
    
    dir_viento_rad = np.radians(values)
    
    # Calculations for the weighted circular mean...
    weighted_sin_sum = np.sum(weights * np.sin(dir_viento_rad))
    weighted_cos_sum = np.sum(weights * np.cos(dir_viento_rad))
    weighted_circular_mean_rad = np.arctan2(weighted_sin_sum, weighted_cos_sum)

    # Conversion from radians to degrees
    weighted_circular_mean_deg = np.degrees(weighted_circular_mean_rad)

    # Ensuring that the mean is within the range of 0 to 360 degrees
    weighted_circular_mean_deg = weighted_circular_mean_deg % 360

    result = weighted_circular_mean_deg
    return result

################################################################################################

# wind weighted average function 
def weighted_wind_average(df, ws_col1, dir_col1, ws_col2, dir_col2):

    import numpy as np # no la toma de la definición global    
    """
    Calculate the weighted circular average of wind directions and the resultant wind speed.

    Parameters:
    df (pd.DataFrame): DataFrame containing wind speed and direction data.
    ws_col1 (str): Column name for the first wind speed.
    dir_col1 (str): Column name for the first wind direction.
    ws_col2 (str): Column name for the second wind speed.
    dir_col2 (str): Column name for the second wind direction.

    Returns:
    pd.DataFrame: DataFrame with added columns 'dir100_avg' and 'ws100_avg'.
    """
    # Convert directions to radians
    dir1_rad = np.deg2rad(df[dir_col1])
    dir2_rad = np.deg2rad(df[dir_col2])

    # Compute weighted vector components
    x1 = df[ws_col1] * np.cos(dir1_rad)
    y1 = df[ws_col1] * np.sin(dir1_rad)
    x2 = df[ws_col2] * np.cos(dir2_rad)
    y2 = df[ws_col2] * np.sin(dir2_rad)

    # Sum of components
    x_sum = x1 + x2
    y_sum = y1 + y2

    # Compute average vector components
    #x_avg = x_sum / 2
    #y_avg = y_sum / 2

    # Compute resultant wind speed by averaging components
    # ws100_avg = np.sqrt(x_avg**2 + y_avg**2)
    ws100_avg = (df[ws_col1] + df[ws_col2])/2 #promedio simple sin tener en cuenta la dir viento

    
    # Compute average direction in radians
    avg_dir_rad = np.arctan2(y_sum, x_sum)

    # Convert back to degrees
    avg_dir_deg = np.rad2deg(avg_dir_rad)

    # Adjust range to [0, 360]
    avg_dir_deg = (avg_dir_deg + 360) % 360

    # Add to dataframe
    df['dir100_avg'] = avg_dir_deg
    df['ws100_avg'] = ws100_avg

    return df

################################################################################################

# wind average function 

def wind_average(df, ws_col1, dir_col1, ws_col2, dir_col2):
  
    import numpy as np # no la toma de la definición global    
    """
    Calculate the weighted circular average of wind directions and the resultant wind speed.

    Parameters:
    df (pd.DataFrame): DataFrame containing wind speed and direction data.
    ws_col1 (str): Column name for the first wind speed.
    dir_col1 (str): Column name for the first wind direction.
    ws_col2 (str): Column name for the second wind speed.
    dir_col2 (str): Column name for the second wind direction.

    Returns:
    pd.DataFrame: DataFrame with added columns 'dir100_avg' and 'ws100_avg'.
    """
        
    # Convert directions to radians
    dir1_rad = np.deg2rad(df[dir_col1])
    dir2_rad = np.deg2rad(df[dir_col2])

    # Compute average direction in radians without weighting by wind speed
    avg_dir_rad = np.arctan2(
        np.sin(dir1_rad) + np.sin(dir2_rad),
        np.cos(dir1_rad) + np.cos(dir2_rad)
    )

    # Convert back to degrees
    avg_dir_deg = np.rad2deg(avg_dir_rad)

    # Adjust range to [0, 360]
    avg_dir_deg = (avg_dir_deg + 360) % 360

    # Compute simple average wind speed
    ws100_avg = (df[ws_col1] + df[ws_col2]) / 2

    
    # Add to dataframe
    df['dir100_avg'] = avg_dir_deg
    df['ws100_avg'] = ws100_avg

    return df


