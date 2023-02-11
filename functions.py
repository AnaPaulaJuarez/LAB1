# -*- coding: utf-8 -*-

# -- Sheet --


"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Laboratorio 1. Inversión de Capital                                                        -- #
# -- script: functions.py : script de python con las funciones generales                                 -- #
# -- author:  ANA VALERIA ARAIZA PERALTA/ANA PAULA JUAREZ REDONDO                                                                      -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository:                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""


# Configuraciones
!pip install yfinance
!pip install PyPortfolioOpt

import pandas as pd
pd.set_option('display.float_format', lambda x: '%.4f' % x)
import yfinance as yf
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns


def obtener_precios(fecha_inicio: str, fecha_fin: str, posiciones: pd.DataFrame): #La siguiente funcion es para sacar los precios, tomando en cuenta las fechas y posiciones
    tickers_a_excluir = ["KOFL", "KOFUBL", "USD", "BSMXB", "NMKA"] #Definimos lista de strings
    tickers = {posiciones.loc[i, "Ticker"].replace("*", "").replace(".", "-") + ".MX": #Definimos diccionario, obtenemos el valor en el DataFrame posiciones en la fila i y columna "Ticker", y reemplazamos el carácter "*" con un espacio vacío y el carácter "." con un guión. 
               #Finalmente, agregamos la cadena ".MX".
               posiciones.loc[i, "Peso (%)"] / 100 for i in range(len(posiciones)) if posiciones.loc[i, "Ticker"] not in tickers_a_excluir} #Obtenemos el valor en la columna "Peso (%)" y dividimos por 100.

    precios = pd.DataFrame() #Creamos DataFrame 
    for t in tickers.keys():
        precios[t] = yf.download(t, start=fecha_inicio, end=fecha_fin, progress=False)["Adj Close"] #Descargamos precios ajustados ("Adj Close") y se asignan al DataFrame con el nombre del Ticker
        
    precios.dropna(axis=1, inplace=True) #Eliminamos columnas con valores faltantes
    precios_mensuales = precios[precios.index.to_series().diff().dt.days > 28] #Precios que tienen una diferencia en días mayor a 28

    return precios, precios_mensuales, tickers

    





