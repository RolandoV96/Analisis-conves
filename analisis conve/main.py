#main
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_functions import verificacion_archivo
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
        tipo_archivo = st.radio(
        "Seleccione el tipo de archivo",
        ["CSV", "XlsX"],
        index=None,
    )
        uploaded_file = st.file_uploader("Drop it like its hot", type=tipo_archivo)
        if tipo_archivo is None:
            st.warning("Por favor, seleccione un tipo de archivo para continuar")
            st.stop()  # Detiene la ejecución aquí

        if uploaded_file is not None:
            if 'uploaded_file_name' not in st.session_state or st.session_state.uploaded_file_name != uploaded_file.name:
                data, validacion = verificacion_archivo(uploaded_file, tipo_archivo)
                st.session_state.data = data  # Guardar en session_state
                st.session_state.uploaded_file_name = uploaded_file.name
                st.toast(validacion)
            else:
                # Usar datos existentes del session_state
                data = st.session_state.data
        
            # Mostrar información básica
            try:
                diag = diagnostico(data)
                st.subheader('Información del Archivo')
            
            
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
                ("float64", "date time", "int64"),
                index=None,
                placeholder="Seleccione el tipo de dato"
                )
                
                result= st.button("Aplicar")
                if result:
                    if column_name == None or target_type == None:
                        st.warning("favor de seleccionar columna y/o tipo")
                    else:
                        change, verificacion = verificacion_previo_cambio(st.session_state.data, column_name, target_type)
                        st.session_state.data = change  # Actualizar session_state
                        data = st.session_state.data    # Actualizar variable local
                        st.toast(verificacion)
        
            except Exception as e:
                st.error(f"Error al procesar los datos: {e}")
                return
                    
    except NameError:
        st.warning("Favor de subir un archivo primero")
        return
    except Exception as e:
        st.error(f"Error: {e}")
        return

if __name__ == "__main__":
    main()