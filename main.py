import data, functions, visualization
import pandas as pd

def estrategiaInversionPasiva(capital: float, comision: float, fechaInicio: str, fechaFin: str):
    """
    estrategiaInversionPasiva es una función que elabora el testeo de la estrategia de inversión pasiva.
    
    :param capital: Capital inicial.
    :param comision: Comisión.
    :param fechaInicio: Fecha de inicio del backtest.
    :param fechaFin: Fecha de fin del backtest.
    """
    
    datos = data.lecturaDatos(fechaInicio)
    precios, preciosMensuales, tickers = functions.obtener_precios(fechaInicio, fechaFin, datos)
    pos_info_pasiva, cap_evol_pasiva, metricas_pasiva = functions.optimizar_estrategia_pasiva(precios, tickers, capital, comision)
    fig = visualization.visualEstrategia(cap_evol_pasiva)
    
    return pos_info_pasiva, cap_evol_pasiva, metricas_pasiva, fig

def atribucionDesempeño(df_pasiva: pd.DataFrame, df_activa: pd.DataFrame, tasaLibreRiesgo: float):
    """
    atribucionDesempeño es una función que devuelve las medidas de atribución al desempeño de las estrategias de inversión pasiva
    y activa.
    
    Parameters:
    df_pasiva: pandas DataFrame
        DataFrame con información de la estrategia pasiva.
    df_activa: pandas DataFrame
        DataFrame con información de la estrategia activa.
    tasaLibreRiesgo: float
        Tasa libre de riesgo para calcular la atribución al desempeño.
        
    Returns:
    medidas: dict
        Diccionario con las medidas de atribución al desempeño.
    """
    
    medidas = functions.rendimientoAtribuido(df_pasiva, df_activa, tasaLibreRiesgo)
    
    return medidas

