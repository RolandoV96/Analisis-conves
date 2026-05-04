#main
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_functions import diagnostico 
from data_functions import verificacion_previo_cambio 
from data_functions import tipo_columnas 
from config import SEPARADOR

def main():
    st.title('Dashboard de Análisis')
    st.markdown(SEPARADOR)
    
    # Sidebar
    st.sidebar.header('Filtros')
    
    # Cargar datos con manejo de errores
    try:


        data = pd.read_excel('data\PayPal-POS-Sales-By-Product-Report-20251101-20251201.xlsx', skiprows=6)
        
        # Mostrar información básica
        st.subheader('Información del Dataset')
        diag = diagnostico(data)
        
        # Mostrar diagnóstico
        st.write("**Valores faltantes:**")
        st.write(diag['valores_faltantes'])
        
        st.write(f"**Duplicados:** {diag['duplicados_count']} ({diag['duplicados_pct']})")
        
        # Mostrar muestra de datos
        st.subheader('Muestra de Datos')
        st.dataframe(diag['muestra'])

        st.subheader('tipo de Datos')
        estructura= tipo_columnas(data)
        st.dataframe(estructura)

        # cambio de datos
        st.markdown(SEPARADOR)
        st.header('Cambio de datos')
        
        # Seleccionar columnas y tipo de dato para cambiar
        column_name = st.selectbox(
        "nombre de columna",
        data.columns,
        index=None,
        placeholder="Seleccione la columna"
        )
        
        target_type= st.selectbox(
        "tipo de dato",
        ("float64", "date time", "int64", "object" ),
        index=None,
        placeholder="Seleccione el tipo de dato"
        )
        
        result= st.button("Aplicar")
        if result:
            if column_name == None or target_type == None:
                st.write("favor de seleccionar columna y/o tipo")
            else:
                change, verificacion= verificacion_previo_cambio(data,column_name,target_type)
                data = change
                st.write(verificacion)
                st.write(str(data[column_name].dtype))
        
    except FileNotFoundError:
        st.error("No se pudo encontrar el archivo 'tu_archivo.csv'")
        st.info("Por favor, asegúrate de que el archivo existe en el directorio.")
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")

if __name__ == "__main__":
    main()