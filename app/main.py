import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from src.visualizations import grafico_barras_estados



st.title("📊 Dashboard Interactivo Olist")

# Logo y título (opcional)
with st.sidebar:
    st.image("img/logo.png", width=80, )  # Opcional
    st.title("🔍 Navegación")

    # Navegador principal
    seccion = st.radio("Selecciona una sección:", [
        "🏠 Resumen General",
        "📍 Clientes por Estado y Ciudad",
        "📦 Pedidos por Cliente",
        "⏱️ Entregas Tardías",
        "⭐ Opiniones (Reviews)",
        "➕ Métricas Adicionales",
    ])

# Lógica para cada sección
if seccion == "🏠 Resumen General":
    # Título de la sección
    st.title("🏠 Resumen General")

# Breve introducción de la app y Olist
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

elif seccion == "📍 Clientes por Estado y Ciudad":
    st.title("📍 Clientes por Estado y Ciudad")
    # Definir un rango de fechas por defecto (puedes ajustarlo según tus necesidades)
    fecha_inicio_default = datetime(2025, 1, 1)
    fecha_fin_default = datetime(2025, 12, 31)

    # Crear los selectores de fechas
    fecha_inicio = st.date_input("Selecciona la fecha de inicio", value=fecha_inicio_default)
    fecha_fin = st.date_input("Selecciona la fecha de fin", value=fecha_fin_default)

    st.pyplot(grafico_barras_estados(fecha_inicio, fecha_fin))
    
elif seccion == "📦 Pedidos por Cliente":
    st.title("📦 Pedidos por Cliente")
    # Pedidos, % del total, ratio por cliente

elif seccion == "⏱️ Entregas Tardías":
    st.title("⏱️ Análisis de Entregas Tardías")
    # Nº de pedidos tarde, % y diagnóstico

elif seccion == "⭐ Opiniones (Reviews)":
    st.title("⭐ Opiniones de Clientes")
    # Nº de reviews, promedio por estado, sin pedidos tardíos

elif seccion == "➕ Métricas Adicionales":
    st.title("➕ Métricas Adicionales")
    # Cualquier análisis extendido o bonus que decidas agregar
