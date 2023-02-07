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


def descargaPrecios(fechaInicio : "Fecha de inicio del backtest", fechaFin : "Fecha de fin del backtest", 
                    datos : "Posiciones del NAFTRAC"):
    """
    descargaPrecios es una función que devuelve los precios históricos en temporalidad diaria y mensual 
    para los tickers que componen al índice NAFTRAC en la fecha ingresada.
    """
    tickersFiltro = ["KOFL", "KOFUBL", "USD", "MXN", "BSMXB", "NMKA"]
    tickers = {datos.loc[i, "Ticker"].replace("*", "").replace(".", "-") + ".MX":
               datos.loc[i, "Peso (%)"] / 100 for i in range(len(datos)) if datos.loc[i, "Ticker"] not in tickersFiltro}

    precios = pd.DataFrame()
    for ticker in tickers.keys():
        precios[ticker] = yf.download(ticker, start=fechaInicio, end=fechaFin, progress=False)["Adj Close"]
        
    precios.dropna(axis=1, inplace=True)
    preciosMensuales = precios[precios.index.to_series().diff().dt.days > 28]
    return precios, preciosMensuales, tickers

    





