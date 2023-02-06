# -*- coding: utf-8 -*-

# -- Sheet --

import pandas as pd

# Crear lista de archivos csv
data = ['NAFTRAC_20210129.csv', 'NAFTRAC_20210226.csv', 'NAFTRAC_20210331.csv', 'NAFTRAC_20210430.csv',
             'NAFTRAC_20210531.csv', 'NAFTRAC_20210630.csv', 'NAFTRAC_20210730.csv', 'NAFTRAC_20210831.csv',
             'NAFTRAC_20210930.csv', 'NAFTRAC_20211026.csv', 'NAFTRAC_20211130.csv', 'NAFTRAC_20211231.csv',
             'NAFTRAC_20220126.csv', 'NAFTRAC_20220228.csv', 'NAFTRAC_20220331.csv', 'NAFTRAC_20220429.csv',
             'NAFTRAC_20220531.csv', 'NAFTRAC_20220630.csv', 'NAFTRAC_20220729.csv', 'NAFTRAC_20220831.csv',
             'NAFTRAC_20220930.csv', 'NAFTRAC_20221031.csv', 'NAFTRAC_20221130.csv', 'NAFTRAC_20221230.csv',
             'NAFTRAC_20230125.csv']

# Hacer lista de dataframes
df_list = [pd.read_csv(file, skiprows=2) for file in data]

# Concatenar la lista verticalmente
vertical_concat = pd.concat(df_list, axis=0)

# Agrupar los Ticker y contar el numero de veces que se repiten
cant = vertical_concat.groupby(['Ticker'])['Ticker'].count().to_frame()

# Filtrar solamente los tickers que se repiten 25 veces 
occurrences = cant[cant['Ticker'] == 25]
occurrences

# Sumar para sacar el total de tickers que se repitieron
cant = vertical_concat.groupby(['Ticker'])['Ticker'].count().to_frame()
cant24 = cant[cant['Ticker'] == 25]
total_tickers = cant24['Ticker'].sum()
print(f'El total de tickers que se repitieron 25 veces son: {total_tickers/25-1}')

