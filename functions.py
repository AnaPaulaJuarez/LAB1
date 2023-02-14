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


def obtener_precios(fecha_inicio: str, fecha_fin: str, posiciones: pd.DataFrame): #La siguiente funcion es para sacar los precios, tomando en cuenta las fechas y posiciones
    tickers_a_excluir = ["KOFL", "KOFUBL", "USD", "BSMXB", "NMKA",'MXN'] #Definimos lista de strings
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
    pos_info_pasiva["Acciones"] = np.floor(list(capital) * tickers / (precios.iloc[0] * (1 + comision))) #Clcula la cantidad de acciones que se pueden comprar con el capital inicial teniendo en cuenta la comisión
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


