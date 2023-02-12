import data, functions, visualization


def estrategiaInversionPasiva(capital : "Capital inicial", comision : "Comisión", 
                              fechaInicio : "Fecha de inicio del backtest", fechaFin : "Fecha de fin del backtest"):
    """
    estrategiaInversionPasiva es una función que elabora el testeo de la estrategia de inversión pasiva.
    
    """
    
    datos = data.lecturaDatos(fechaInicio)
    precios, preciosMensuales, tickers = functions.descargaobtener_precios(fecha_inicio, fecha_fin, posiciones)
    pos_info_pasiva, cap_evol_pasiva, metricas_pasiva = functions.optimizar_estrategia_pasiva(precios, tickers, capital, comision)
    fig = visualization.visualEstrategia(cap_evol_pasiva)
    
    return pos_info_pasiva, cap_evol_pasiva, metricas_pasiva, fig

def atribucionDesempeño(df_pasiva : "Estrategia Pasiva", df_activa : "Estrategia Activa", tasaLibreRiesgo : "Tasa libre riesgo"):
    """
    atribucionDesempeño es una función que devuelve las medidas de atribución al desempeño de las estrategias de inversión pasiva
    y activa.
    
    """
    
    medidas = functions.rendimientoAtribuido(estrategiaA, estrategiaB, tasaRiesgo)
    
    return medidas
