En el presente repositorio encontraran todas las notebooks y datasets desarrollados durante mi trabajo 
de investigacion para elaborar mi Tesis de Maestria sobre prediccion de energia eolica.

Los pronosticos de clima historicos y futuros se extraen y transforman mediante las siguientes notebooks:

1) SMN Meteostat Wheather Data.ipynb: obtiene los datos de pronostico del Servicio Meteorológic Nacional
2) ECMWF Weather Data.ipynb: obtiene los datos de pronostico del ECMWF (European Centre for Medium-Range Weather Forecasts)
3) GFS - Global Forecast System.ipynb: obtiene los datos de pronostico del GFS (Global Forecast System)

(*) Para ECMWF y GFS los archivos con los pronosticos historicos no se encuentra subido debido a su peso,
Pero se pueden descargar directamente desde la web de estos organismos, esta indicado en las notebooks

En las siguientes notebooks se realiza analisis exploratorio de datos y preparacion de datos para
el entrenamiento de los modelos. Asi mismo encontraran la notebook en la que se entrenan todos los
modelos utilizados y la evaluacion se rendimiento:

1) EDA_LAC.ipynb: Se transforman y limpian los datos reales del parque La Castellana I, se consolidan los datos de
   pronosticos obtenidos con las notebooks anteriores y se evalua cual correlaciona mejor con datos reales de parque.
   Se crea el dataset para entrenamiento de los modelos.
2) All Models for Wind Power Prediction.ipynb: Se implementan, entrenan, testean y se ajustan los siguientes modelos
   Sarimax, Prophet, LightGBM y LSTM. Asi mismo, se comparan los rendimientos de cada uno de los modelos.

 Por ultimo, dentro de la carpeta "Modelo en Produccion" encontraran todos los archivos necesarios para llevar 
 adelante el pasaje a produccion del modelo:

 1) Energy Model in Production.ipynb: En esta notebook se guarda y empaqueta el modelo LightGBM y se dejan
    todos los pasos para crear, publicar y correr la imagen en Docker. La cual tambien esta publicada en Docker Hub
 2) energy_app.py, energy_predictions.py: crea la aplicacion para para publicar en servidor web Flask el modelo

 
