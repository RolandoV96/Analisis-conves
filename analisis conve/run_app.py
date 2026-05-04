#run_appy
import subprocess
import sys
import os
import time

def ejecutar_streamlit():
    """Ejecuta la aplicación de Streamlit usando subprocess"""

    print("Iniciando aplicación de Streamlit...")
    print("Dashboard de Análisis La Conve")
    print("-" * 40)

    try:
        # Comando para ejecutar Streamlit
        comando = [
            sys.executable, "-m", "streamlit", "run", 
            "analisis conve\main.py", 
            "--server.port=8501",
            "--server.headless=true"
        ]

        print(f"Ejecutando comando: {' '.join(comando)}")
        print("La aplicación se abrirá en: http://localhost:8501")
        print("  Para detener la aplicación, presiona Ctrl+C")
        print("-" * 40)

        # Ejecutar el proceso
        proceso = subprocess.run(comando, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar Streamlit: {e}")
        print("Asegúrate de que Streamlit esté instalado: pip install streamlit")
    except KeyboardInterrupt:
        print("\n Aplicación detenida por el usuario")
    except Exception as e:
        print(f"Error inesperado: {e}")

def verificar_dependencias():
    """Verifica que las dependencias necesarias estén instaladas"""
    
    print("Verificando dependencias...")
    print("-" * 40)
    
    dependencias_requeridas = [
        'streamlit',
        'pandas', 
        'numpy',
        'matplotlib',
        'seaborn',
        'openpyxl',  # ← Agregamos openpyxl para archivos Excel
        'scipy'      # ← También agregamos scipy que usas en data_utils
    ]
    
    dependencias_faltantes = []
    
    for dependencia in dependencias_requeridas:
        try:
            __import__(dependencia)
            print(f"✓ {dependencia}: Instalado")
        except ImportError:
            print(f"✗ {dependencia}: NO instalado")
            dependencias_faltantes.append(dependencia)
    
    print("-" * 40)
    
    if dependencias_faltantes:
        print("⚠️  DEPENDENCIAS FALTANTES:")
        for dep in dependencias_faltantes:
            print(f"   - {dep}")
        print("\nPara instalar las dependencias faltantes, ejecuta:")
        print(f"pip install {' '.join(dependencias_faltantes)}")
        return False
    else:
        print("✅ Todas las dependencias están instaladas")
        return True

def main():
    """Función principal que coordina la verificación y ejecución"""
    
    print("=" * 50)
    print("DASHBOARD DE ANÁLISIS LA CONVE")
    print("=" * 50)
    
    # Verificar dependencias primero
    if verificar_dependencias():
        print("\n" + "=" * 50)
        ejecutar_streamlit()
    else:
        print("\n No se puede ejecutar la aplicación.")
        print("Por favor, instala las dependencias faltantes y vuelve a intentar.")

if __name__ == "__main__":
    main()