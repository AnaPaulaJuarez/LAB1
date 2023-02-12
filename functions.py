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

import pandas as pd
pd.set_option('display.float_format', lambda x: '%.4f' % x)
import yfinance as yf
import numpy as np
from pypfopt import EfficientFrontier
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
def optimizar_estrategia_pasiva(precios, tickers, capital, comision):

    # Almacenar informacion posiciones iniciales
    pos_info_pasiva = pd.DataFrame(index=precios.columns, columns=["Acciones", "Costo Neto", "Comisión", "Costo Final"])  #DataFrame para almacenar posiciones iniciales 
    
    # Posiciones iniciales
    pos_info_pasiva["Acciones"] = np.floor(capital * tickers / (precios.iloc[0] * (1 + comision))) #Clcula la cantidad de acciones que se pueden comprar con el capital inicial teniendo en cuenta la comisión
    pos_info_pasiva["Costo Neto"] = pos_info_pasiva["Acciones"] * precios.iloc[0] #Se calcula el costo neto de las acciones adquiridas, multiplicando la cantidad de acciones por el precio por acción
    pos_info_pasiva["Comisión"] = pos_info_pasiva["Acciones"] * precios.iloc[0] * comision #Se calcula el costo de la comisión, multiplicando la cantidad de acciones por el precio por acción y la comisión
    pos_info_pasiva["Costo Final"] = pos_info_pasiva["Acciones"] * precios.iloc[0] * (1 + comision) #Costo final = costo neto + la comisión
    pos_info_pasiva["Ponderación"] = pos_info_pasiva["Acciones"] * precios.iloc[0] / capital #Se calcula la ponderación de cada activo, dividiendo el costo neto de cada activo por el capital total invertido
    
    # Guardar información de evo capital
    cap_evol_pasiva = pd.DataFrame(index=precios.index, columns=["Evo Capital", "Rend. Mensual", "Rend. Mensual Acum."]) #Creamos DataFrame para guardar la información sobre la evolucion del capital 
    
    # Prueba
    cap_evol_pasiva["Evo Capital"] = (precios * pos_info_pasiva["Acciones"].values).sum(axis=1) #Multiplicamos los precios de cada acción * cantidad de acciones que se han comprado y sumando los resultados para cada día
    cap_evol_pasiva["Rend. Mensual"] = cap_evol_pasiva["Evo Capital"].pct_change().dropna() #Se calcula el rend mensual como el porcentaje de cambio en la evolución del capital de un mes a otro
    cap_evol_pasiva["Rend. Mensual Acum."] = (cap_evol_pasiva["Rend. Mensual"] + 1).cumprod() - 1  #Sacamos el porcentaje acumulado de crecimiento del capital
    
    # Métricas
    cap_inv = pos_info_pasiva["Costo Final"].sum() #Calculamos el capital invertido en la estrategia de inversión pasiva sumando el costo final de cada posición
    metricas_pasiva = pd.DataFrame({"Capital Inicial": capital, "Capital Invertido": cap_inv, "Efectivo": capital - cap_inv, "Capital Final": capital - cap_inv + cap_evol_pasiva["Evo Capital"].iloc[-1], "Rend. Efectivo %": cap_evol_pasiva["Rend. Mensual Acum."].iloc[-1] * 100}, index=["Estrategia Pasiva"])  
    
    return pos_info_pasiva, cap_evol_pasiva, metricas_pasiva

def inversionActivaEficiente(datosDivisionFecha: "Fecha de partición de datos", 
                    diarioPrecios: "Precios diarios", preciosMensuales: "Precios mensuales", 
                    fondos: "Capital", tarifaComision: "Comisión"):
    
    # Portafolio eficiente (Sharpe)
    preciosDivisados = diarioPrecios[diarioPrecios.index <= datosDivisionFecha]
    rendimientoEsperado = expected_returns.mean_historical_return(preciosDivisados, compounding = False, log_returns = True)
    covarianza = risk_models.sample_cov(preciosDivisados, log_returns = True)
    portafolioEficiente = EfficientFrontier(rendimientoEsperado, covarianza)
    pesos = portafolioEficiente.max_sharpe()
    pesosDataFrame = pd.DataFrame(pesos, columns = list(pesos.keys()), index = ["Ponderaciones"])
    pesosDataFrame = pesosDataFrame[pesosDataFrame > 0].dropna(axis = 1)
    
    # Posiciones iniciales
    informacionInversionActiva = pd.DataFrame(index = pesosDataFrame.columns, columns = ["Títulos", "Costo de Compra Bruto", "Comisión",
                                                                      "Costo de Compra Total", "Ponderación"])
    preciosDespuesFecha = diarioPrecios.loc[diarioPrecios.index > datosDivisionFecha, list(pesosDataFrame.keys())]
    preciosMensualesDespuesFecha = preciosMensuales.loc[preciosMensuales.index > datosDivisionFecha, list(pesosDataFrame.keys())]
    preciosMensualesDataFrame = pd.DataFrame()
    preciosMensualesDataFrame.loc[preciosDespuesFecha.index[0], preciosMensualesDespuesFecha.columns] = preciosDespuesFecha.iloc[0, :]

    for i in range(len(preciosMensualesDespuesFecha)):
        preciosMensualesDataFrame.loc[preciosMensualesDespuesFecha.index[i], preciosMensualesDespuesFecha.columns] = preciosMensualesDespuesFecha.iloc[i, :]

    for ticker in pesosDataFrame.columns:
        informacionInversionActiva.loc[ticker, "Títulos"] = np.floor((fondos * pesosDataFrame.loc["Ponderaciones", ticker]) / 
                                                                    (preciosMensualesDataFrame.loc[preciosMensualesDataFrame.index[0], ticker] * (1 + tarifaComision)))
        informacionInversionActiva.loc[ticker, "Costo de Compra Bruto"] = informacionInversionActiva.loc[ticker, "Títulos"] * preciosMensualesDataFrame.loc[preciosMensualesDataFrame.index[0], ticker]
        informacionInversionActiva.loc[ticker, "Comisión"] = informacionInversionActiva.loc[ticker, "Títulos"] * preciosMensualesDataFrame.loc[preciosMensualesDataFrame.index[0], ticker] * tarifaComision
        informacionInversionActiva.loc[ticker, "Costo de Compra Total"] = informacionInversionActiva.loc[ticker, "Títulos"] * preciosMensualesDataFrame.loc[preciosMensualesDataFrame.index[0], ticker] * (1 + tarifaComision)
        informacionInversionActiva.loc[ticker, "Ponderación"] = (informacionInversionActiva.loc[ticker, "Títulos"] * preciosMensualesDataFrame.loc[preciosMensualesDataFrame.index[0], ticker]) / fondos

    return informacionInversionActiva

def backtest(datosDivisionFecha, diarioPrecios, preciosMensuales, fondos, tarifaComision, benchmark_returns):
    # Ejecutar la función inversionActivaEficiente
    informacionInversionActiva = inversionActivaEficiente(datosDivisionFecha, diarioPrecios, preciosMensuales, fondos, tarifaComision)
    
    # Calcular rendimientos del portafolio y del benchmark
    preciosMensualesDespuesFecha = preciosMensuales.loc[preciosMensuales.index > datosDivisionFecha, informacionInversionActiva.index]
    rendimientosPortafolio = (preciosMensualesDespuesFecha / preciosMensualesDespuesFecha.iloc[0, :]).prod() - 1
    rendimientosBenchmark = (benchmark_returns.loc[preciosMensualesDespuesFecha.index] / benchmark_returns.loc[preciosMensualesDespuesFecha.index[0]]).prod() - 1
    
    # Calcular la tasa de rendimiento esperada y la volatilidad del portafolio
    tasaRendimientoEsperada = rendimientosPortafolio.mean()
    volatilidad = rendimientosPortafolio.std()
    
    # Calcular la tasa de rendimiento esperada y la volatilidad del benchmark
    tasaRendimientoEsperadaBenchmark = rendimientosBenchmark.mean()
    volatilidadBenchmark = rendimientosBenchmark.std()
    
    # Calcular el Sharpe ratio del portafolio y del benchmark
    sharpeRatio = (tasaRendimientoEsperada - 0.03) / volatilidad
    sharpeRatioBenchmark = (tasaRendimientoEsperadaBenchmark - 0.03) / volatilidadBenchmark

    # Graficar los rendimientos del portafolio y del benchmark
    plt.plot(rendimientosPortafolio.index, rendimientosPortafolio, label="Portafolio")
    plt.plot(rendimientosBenchmark.index, rendimientosBenchmark, label="Benchmark")
    plt.xlabel("Fecha")
    plt.ylabel("Rendimiento")
    plt.legend()
    plt.show()

def rendimientoAtribuido(estrategiaA : pd.DataFrame, estrategiaB : pd.DataFrame, tasaRiesgo : float):

    resultados = pd.DataFrame(index = ["prom_mensual", "acum_mensual", "ratio_sharpe"], columns = ["Descripción", "Estrategia A", "Estrategia B"]) #Creamos un nuevo DataFrame "RESULTADOS"
    resultados.loc["prom_mensual", "Descripción"] = "Rend Prom mensual" #Asignamos valores a las celdas
    resultados.loc["acum_mensual", "Descripción"] = "Rend mensual acum" #Asignamos valores a las celdas
    resultados.loc["ratio_sharpe", "Descripción"] = "Ratio Sharpe" #Asignamos valores a las celdas

    #Estrategia A 
    resultados.loc["prom_mensual", "Estrategia A"] = estrategiaA["Rend Mensual"].dropna().mean() #Calculamos el rend promedio mensual y asignamos los valores a las celdas correspondientes en el DataFrame
    resultados.loc["acum_mensual", "Estrategia A"] = estrategiaA["Rend Mensual Acum"][-1] #Calculamos el rend promedio acumulado y asignamos los valores a las celdas correspondientes en el DataFrame
    resultados.loc["ratio_sharpe", "Estrategia A"] = (estrategiaA["Rend Mensual"].dropna().mean() - tasaRiesgo) / estrategiaA["Rend Mensual"].dropna().std() #Calculamos el ratio sharpe y asignamos los valores a las celdas correspondientes en el DataFrame
   
    #Estrategia B
    resultados.loc["prom_mensual", "Estrategia B"] = estrategiaB["Rend Mensual"].dropna().mean()
    resultados.loc["acum_mensual", "Estrategia B"] = estrategiaB["Rend Mensual Acum"][-1]
    resultados.loc["ratio_sharpe", "Estrategia B"] = (estrategiaB["Rend Mensual"].dropna().mean() - tasaRiesgo) / estrategiaB["Rend Mensual"].dropna().std() 

    return resultados








