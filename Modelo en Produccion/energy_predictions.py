#!/usr/bin/env python3
#import numpy as np

import os
import pickle
import pandas as pd

# LightGBM model
import lightgbm as lgb
from lightgbm import LGBMRegressor

FOLDER = 'dist'


def fetch_pickle(folder: str, file_name: str):
    print(f'Loading {file_name} from local')    
    with open(os.path.join(folder, file_name), 'rb') as f:
        fetched_object = pickle.load(f)

    return fetched_object    


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
        devuelve las predicciones para las variables exogenas df_exog.
    """
    # Fetch model
    model = get_model()

    # Predict on test data
    pred_energia = model.predict(df_exog)

    return pred_energia
