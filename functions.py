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




    





