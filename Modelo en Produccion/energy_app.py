import warnings
warnings.filterwarnings('ignore')

from flask import Flask, request, jsonify
import pandas as pd
import requests
import energy_predictions as pr  # Módulo donde está la función `predict`

from io import StringIO

app = Flask(__name__)

# URL predeterminada si no se proporciona ninguna en el método GET
DEFAULT_CSV_URL = "https://raw.githubusercontent.com/guilledesimone/MMA-Tesis/refs/heads/main/Datos/ds_exog.csv"

def load_and_validate_csv(df_exog):
    """
    Valida que el DataFrame tenga la estructura esperada.
    """
    # Columnas esperadas
    expected_columns = ['FechaHora', 'aeros_disp', 'ws100_avg', 'dir100_avg', 'temp_avg']

    # Validar que el archivo contenga las columnas esperadas
    missing_columns = [col for col in expected_columns if col not in df_exog.columns]
    if missing_columns:
        return False, f'Missing expected columns: {missing_columns}'

    # Validar que las columnas exógenas sean numéricas (excepto "FechaHora")
    non_numeric_columns = [col for col in expected_columns[1:] if not pd.api.types.is_numeric_dtype(df_exog[col])]
    if non_numeric_columns:
        return False, f'Columns must contain numeric values: {non_numeric_columns}'

    return True, None

def make_prediction(df_exog):
    """
    Realiza la predicción usando el DataFrame validado y devuelve el resultado.
    """
    try:
        predictions = pr.predict(df_exog)
    except Exception as e:
        return None, f'Prediction error: {str(e)}'
    
    # Crear un DataFrame para las predicciones
    df_predictions = pd.DataFrame({
        'FechaHora': df_exog['FechaHora'],
        'predicted_energy': predictions
    })
    return df_predictions, None

@app.route("/")
def hello():
    return jsonify(message="Hello! I'm the Energy Predictor")

@app.route('/energy_pred/upload', methods=['POST'])
def energy_pred_upload():
    """
    Predice la energía basado en un archivo CSV cargado en la solicitud.
    """
    # Intentar obtener el archivo CSV desde la solicitud
    file = request.files.get('file', None)

    if not file or file.filename == '':
        return jsonify(message="No file provided"), 400

    # Cargar el archivo CSV como un DataFrame de pandas
    try:
        df_exog = pd.read_csv(file)
    except Exception as e:
        return jsonify(message=f"Error reading file: {str(e)}"), 400

    # Validar el archivo CSV
    is_valid, error_message = load_and_validate_csv(df_exog)
    if not is_valid:
        return jsonify(message=error_message), 400

    # Realizar la predicción
    predictions, error_message = make_prediction(df_exog)
    if predictions is None:
        return jsonify(message=error_message), 500

    return jsonify(predictions=predictions.to_dict(orient='records'))

@app.route('/energy_pred/url', methods=['GET'])
def energy_pred_url():
    """
    Predice la energía basado en un archivo CSV descargado desde una URL proporcionada.
    """
    # Obtener la URL desde los parámetros de la consulta (o usar la URL predeterminada)
    csv_url = request.args.get('url', DEFAULT_CSV_URL)

    # Descargar el archivo CSV desde la URL proporcionada
    try:
        response = requests.get(csv_url)
        response.raise_for_status()  # Levanta una excepción si ocurre un error
        df_exog = pd.read_csv(StringIO(response.text)) 
        #df_exog = pd.read_csv(pd.compat.StringIO(response.text))
    except Exception as e:
        return jsonify(message=f"Error retrieving file from URL: {str(e)}"), 400

    # Validar el archivo CSV
    is_valid, error_message = load_and_validate_csv(df_exog)
    if not is_valid:
        return jsonify(message=error_message), 400

    # Realizar la predicción
    predictions, error_message = make_prediction(df_exog)
    if predictions is None:
        return jsonify(message=error_message), 500

    return jsonify(predictions=predictions.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
