#!/usr/bin/env python3
import numpy as np

import os
import pickle


# LightGBM model
import lightgbm as lgb
from lightgbm import LGBMRegressor


### VER SI HACE FALTA
import pandas as pd
import numpy as np

pd.options.mode.copy_on_write = True 
from datetime import datetime, timedelta

from sklearn.metrics import mean_absolute_error, mean_squared_error#, r2_score
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit
### HASTA ACA - VER SI HACE FALTA



#from sklearn.preprocessing import LabelEncoder
#from tensorflow.keras.models import model_from_json
#from config import *
#import aws_utils as au

""" Fetch trained models, encoders and tokenizers. Make predictions. """
def fetch_pickle(folder: str, file_name: str):
    # TODO Part 2 
    # bucket_name: str,
    # au.download_pickle_from_s3(bucket_name, folder, file_name)
    # Load normalizer from local
    print(f'Loading {file_name} from local')    
    with open(os.path.join(folder, file_name), 'rb') as f:
        fetched_object = pickle.load(f)

    return fetched_object    

#def get_model_and_encoders():
#    print('Fetching binaries')
#    normalizer = fetch_pickle(BUCKET_NAME, FOLDER, 'normalizer.pkl')
#    encoder = fetch_pickle(BUCKET_NAME, FOLDER, 'encoder.pkl')
#    model = fetch_pickle(BUCKET_NAME, FOLDER, 'model.pkl')
#    return normalizer, encoder, model

def get_model():
    print('Fetching binaries')
    model = fetch_pickle(FOLDER, 'model.pkl')
    return model


def predict(df_exog: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza predicciones utilizando un modelo previamente cargado y devuelve un DataFrame con las predicciones.

    Args:
        df_exog (pd.DataFrame): DataFrame con las características externas (las entradas del modelo).

    Returns:
        pd.DataFrame: DataFrame con las predicciones y el índice como columna 'FechaHora'.
    """
    # Fetch model
    model = get_model()

    # Predict on test data
    pred_energia = model.predict(df_exog)

    # Create a DataFrame with the predictions
    df_pred_energia = pd.DataFrame({
        'FechaHora': df_exog.index,
        'pred_energia': pred_energia
    })

    return df_pred_energia




'''
def get_deep_model():
    print('Loading deep model from disk')

    # Model definition
    file_name = 'model.json'
    au.download_json_from_s3(BUCKET_NAME, FOLDER, file_name)    
    with open(os.path.join(FOLDER, file_name), 'r') as json_file:
        model = model_from_json(json_file.read())
    print('Model definition loaded from disk')

    # Model weights
    file_name = 'model.h5'
    au.download_h5py_from_s3(BUCKET_NAME, FOLDER, file_name)    
    model.load_weights(os.path.join(FOLDER, file_name))
    print("Model weights loaded from disk")

    return model
    '''