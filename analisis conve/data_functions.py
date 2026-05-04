# data_functions.py
import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu, anderson, spearmanr
import io
from contextlib import redirect_stdout


def verificacion_archivo(archivo,tipo):
    if tipo == "XlsX":
        df = pd.read_excel(archivo, skiprows=6)
        validado= f"se abrio archivo {tipo}"
    elif tipo =="CSV": 
        df = pd.read_csv(archivo, skiprows=6)
        validado= f"se abrio archivo {tipo}"
    else:
         df = None
         validado = "Error, tipo de dato None"
    return df,validado

# Hace la revision de los datos iniciales
def diagnostico(df):
    """Función para diagnóstico completo de DataFrame"""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        df.info()
    info_capturada = buffer.getvalue()

    info = {
        'estructura': info_capturada,
        'valores_faltantes': (100 * df.isna().sum() / df.shape[0]).apply(lambda x: f"{x:.2f}%"),
        'duplicados_count': df.duplicated(keep=False).sum(),
        'duplicados_pct': f"{100 * df[df.duplicated(keep=False)].shape[0] / df.shape[0]:.2f}%",
        'muestra': df.sample(5) if len(df) > 5 else df.head(),
        'descripcion': df.describe()
    }
    return info

# bucle para crear una tabla y verificar el nombre de la columna y su tipo de dato
def tipo_columnas(df):
    filas = []
    for columna in df.columns:
        fila = {"Columna": columna, "Tipo de dato": str(df[columna].dtype)}
        filas.append(fila)
        df_tabla = pd.DataFrame(filas)
    return df_tabla

# verifica si la columna ya es del tipo de datos solicitado si no manda hacer el cambio
def verificacion_previo_cambio(df,column_name,target_type):
    valor=df[column_name].dtype
    if str(valor)==target_type:
       validado = "Columna ya del tipo seleccionado"
       return df,validado
    else:
        type_functions = {
        "float64": change_float,
        "int64": change_int,
        "date time":change_date_time
    }
        type_function = type_functions.get(target_type)
        if type_function:
            return type_function(df,column_name), f"se realizo el cambio a {target_type}"
        else:
           validado = "Error, tipo de dato None"
    return df,validado

# cambia a date time el tipo de dato de la columna y Dataframe esecificados
def change_date_time(df, column_name):
    df[column_name]=pd.to_datetime(df[column_name], errors="coerce")
    return df

# cambia a entero el tipo de dato de la columna y Dataframe esecificados
def change_int(df, column_name):
    df[column_name] = pd.to_numeric(df[column_name], errors="coerce").astype("Int64")
    return df

# cambia a tipo float el tipo de dato de la columna y Dataframe esecificados
def change_float(df, column_name):
    df[column_name] = pd.to_numeric(df[column_name], errors="coerce")
    return df
