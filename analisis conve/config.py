# config.py
import warnings
import pandas as pd
import numpy as np
import random

# ==================== CONFIGURACIÓN =======================
CONST_SEED = 22
np.random.seed(CONST_SEED)
random.seed(CONST_SEED)

# ===== Configuración de pandas y warnings =================
warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None
pd.set_option("display.width", 5000)
pd.set_option("display.max_columns", 20000)
pd.set_option("display.max_colwidth", None)

# Separador para mejorar la lectura de datos
SEPARADOR = "---"