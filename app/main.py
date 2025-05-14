# Importaciones para que la aplicacion encuentre las rutas
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importaciones de librerias
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Importaciones de metodos de otras clases
from src.visualizations import clientes_estado
from src.analysis import tabla_ciudades
from src.visualizations import pedidos_por_ciudad
from src.visualizations import pedidos_con_retraso

# Definicion de la sidebar
def sidebar():
        
    with st.sidebar:
        
        # Logo y título del sidebar
        st.image("img/logo.png", width=80, )  # Opcional
        st.title("🔍 Navegación")

        # Secciones del dashboard
        seccion = st.radio("Selecciona una sección:", [
            "🏠 Inicio",
            "📍 Clientes, Estados y Ciudades",
            "📦 Pedidos, Ciudades y Clientes",
            "⏱️ Pedidos con Retraso",
            "⭐ Opiniones (Reviews)",
            "➕ Métricas Adicionales",
        ])
    
    selector_secciones(seccion)

# Logica para el selector de las secciones de la aplicacion
def selector_secciones(seccion):

    if seccion == "🏠 Inicio":

        st.title("📊 Dashboard Interactivo Olist")

        st.write("""
        Bienvenido a la **aplicación de análisis de Olist**, diseñada para proporcionarte **información detallada** sobre el comportamiento de los **clientes**, los **pedidos**, y las **opiniones** que los usuarios dejan acerca de los productos.
        
        Olist es una plataforma de **e-commerce** que permite a los vendedores brasileños vender sus productos a través de un marketplace de ventas. Esta aplicación te ayudará a analizar las métricas clave para mejorar la toma de decisiones y entender los patrones detrás de las compras.

        ### Funcionalidades
        Esta aplicación incluye un análisis interactivo donde podrás explorar datos sobre:
        - **Clientes por estado y ciudad**
        - **Pedidos realizados por cliente y análisis del ratio de compras**
        - **Tiempos de entrega y análisis de retrasos**
        - **Reseñas de clientes y puntuaciones por estado**

        ### Guía rápida
        1. **Clientes por Estado y Ciudad**: Obtén la distribución de clientes según su ubicación.
        2. **Pedidos por Cliente**: Analiza el número de pedidos por cliente y sus ratios.
        3. **Entregas Tardías**: Identifica problemas de retrasos en la entrega por ciudad.
        4. **Opiniones de Clientes**: Explora las reseñas y la puntuación promedio por estado, excluyendo los pedidos con retraso.

        Para comenzar, usa el menú en el **sidebar** y selecciona el análisis que desees explorar.
        """)
        
        total_clientes = 35000
        total_pedidos = 250000
        pedidos_tarde = 5000
        reviews_promedio = 4.3

        st.subheader("📊 Métricas clave")
        st.write(f"- **Total de clientes**: {total_clientes}")
        st.write(f"- **Total de pedidos**: {total_pedidos}")
        st.write(f"- **Pedidos con retraso**: {pedidos_tarde} ({(pedidos_tarde / total_pedidos) * 100:.2f}%)")
        st.write(f"- **Puntuación promedio de reviews**: {reviews_promedio} ⭐")

        # Incluir gráficos pequeños, si es necesario (ejemplo con Matplotlib)
        import matplotlib.pyplot as plt
        import numpy as np

        # Gráfico simple de ejemplo (evolución de pedidos en el tiempo)
        fig, ax = plt.subplots(figsize=(10, 5))
        fechas = pd.date_range(start="2023-01-01", end="2023-12-31", freq="M")
        pedidos = np.random.randint(10000, 25000, size=len(fechas))
        ax.plot(fechas, pedidos, marker="o", color="green")
        ax.set_title("Evolución mensual de pedidos")
        ax.set_xlabel("Mes")
        ax.set_ylabel("Número de pedidos")
        ax.grid(True)

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)

    elif seccion == "📍 Clientes, Estados y Ciudades":
        st.title("📍 Clientes, Estados y Ciudades")
        st.write("En esta seccion se encuentran gráficos relacionados a los clientes, estados y ciudades.\n Los gráficos son reactivos a los cambios en los campos de fechas ubicados antes de los mismos.")
        st.markdown("---")
        
        st.subheader("Campos para modificar el rango de fechas:")

        # Definir un rango de fechas por defecto
        fecha_inicio_default = datetime(2000, 1, 1)
        fecha_fin_default = datetime(2025, 12, 31)

        # Crear los selectores de fechas
        fecha_inicio = st.date_input("Selecciona la fecha de inicio", value=fecha_inicio_default)
        fecha_fin = st.date_input("Selecciona la fecha de fin", value=fecha_fin_default)
        st.markdown("---")
        
        # Grafico de barras de numeros de clientes por estado
        st.subheader("Gráfico de barras Número de Clientes por Estado:")
        st.pyplot(clientes_estado(fecha_inicio, fecha_fin))
        st.markdown("---")
        
        # Tabla de numeros de clientes por ciudad
        st.subheader("Tabla Número de Clientes por Ciudad:")
        st.write(tabla_ciudades(fecha_inicio, fecha_fin))
        st.markdown("---")

    elif seccion == "📦 Pedidos, Ciudades y Clientes":
        st.title("📦 Pedidos y Clientes")
        st.write("En esta seccion se encuentra el análisis relacionado con los pedidos y clientes de la tienda.\n Existen campos modificables por el usuario para visualizar cambios en los gráficos en tiempo real.")
        st.markdown("---")
        
        st.subheader("Campos para modificar la información del gráfico:")
        # Sidebar con filtros
        top_n = st.slider("Selecciona el número de ciudades a mostrar", 5, 10, 20)
        
        criterio = st.selectbox(
            "Ordenar ciudades por",
            options=['num_pedidos', 'porcentaje_pedidos', 'ratio_pedidos_cliente'],
            format_func=lambda x: {
                'num_pedidos': "Número de pedidos",
                'porcentaje_pedidos': "Porcentaje de pedidos",
                'ratio_pedidos_cliente': "Pedidos por cliente (ratio)"
            }[x]
        )
        st.markdown("---")
        
        grafico, df = pedidos_por_ciudad(top_n, criterio)
        
        # Grafico de barras de numeros de clientes por estado
        st.subheader("Gráfico de barras Pedidos por Ciudad:")
        st.text("Este gráfico de barras muestra información relacionado con los pedidos en cada ciudad, puede mostrar diferente información dependiendo de lo seleccionado por el usuario anteriormente")
        st.pyplot(grafico)
        st.markdown("---")
        
        # Tabla de numeros de clientes por ciudad
        st.subheader("Tabla con toda la información del análisis:")
        st.write(df)
        st.markdown("---")

    elif seccion == "⏱️ Pedidos con Retraso":
        st.title("⏱️ Análisis de Pedidos con Retraso")
        st.write("En esta seccion se encuentra el análisis relacionado con los pedidos que cuentan con un retraso en su envío.\n Existen campos modificables por el usuario para visualizar cambios en los gráficos en tiempo real.")
        st.markdown("---")
        
        # Grafico de barras de numeros de clientes por estado
        st.subheader("Gráfico de barras Pedidos por Ciudad:")
        st.text("Este gráfico de barras muestra información relacionado con los pedidos en cada ciudad, puede mostrar diferente información dependiendo de lo seleccionado por el usuario anteriormente")
        
        st.markdown("---")
        
        pedidos_con_retraso()

    elif seccion == "⭐ Opiniones (Reviews)":
        st.title("⭐ Opiniones de Clientes")
        # Nº de reviews, promedio por estado, sin pedidos tardíos

    elif seccion == "➕ Métricas Adicionales":
        st.title("➕ Métricas Adicionales")
        # Cualquier análisis extendido o bonus que decidas agregar

sidebar()
