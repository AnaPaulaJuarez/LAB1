
import pandas as pd
import numpy as np

def lecturaDatos(fecha: str) :
    """
    lecturaDatos es una función que lee el archivo de Excel que contiene las posiciones del NAFTRAC para la fecha deseada.
    
    """
    
    datos = pd.read_csv("files/NAFTRAC_" + fecha.replace("-", "") + ".csv", skiprows=2).dropna()
    
    return datos
