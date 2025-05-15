# Importaciones para que la aplicacion encuentre las rutas
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importaciones de metodos de otras clases
from src.visualizations import pedidos_opiniones
from src.visualizations import pedidos_con_retraso as vis_pedidos_con_retraso
from src.visualizations import pedidos_por_ciudad
from src.analysis import tabla_ciudades
from src.analysis import get_estados
from src.visualizations import clientes_estado
from src.visualizations import top_categorias
from src.visualizations import dia_semana_mayor_ventas

# Importaciones de librerias
from datetime import datetime
import streamlit as st

# Metodo que carga la pantalla de inicio
def inicio():
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

# Metodo que carga la pantalla con el analisis relacionado con los clientes, los diferentes estados y ciudades
def clientes_estados_ciudades():
    st.title("📍 Clientes, Estados y Ciudades")
    st.write("En esta seccion se encuentran gráficos relacionados a los clientes, estados y ciudades.\n Los gráficos son reactivos a los cambios en los campos de fechas ubicados antes de los mismos.")
    st.markdown("---")

    st.subheader("Campos para modificar el rango de fechas:")

    # Definir un rango de fechas por defecto
    fecha_inicio_default = datetime(2000, 1, 1)
    fecha_fin_default = datetime(2025, 12, 31)

    # Crear los selectores de fechas
    fecha_inicio = st.date_input(
        "Selecciona la fecha de inicio", value=fecha_inicio_default)
    fecha_fin = st.date_input(
        "Selecciona la fecha de fin", value=fecha_fin_default)
    st.markdown("---")

    # Grafico de barras de numeros de clientes por estado
    st.subheader("Gráfico de barras Número de Clientes por Estado:")
    st.pyplot(clientes_estado(fecha_inicio, fecha_fin))
    st.markdown("---")

    # Tabla de numeros de clientes por ciudad
    st.subheader("Tabla Número de Clientes por Ciudad:")
    st.write(tabla_ciudades(fecha_inicio, fecha_fin))
    st.markdown("---")
    
    st.subheader("Análisis Descriptivo:")
    st.write("Hemos observado que las ciudades están muy fragmentadas, hay muchas que solo tienen uno o muy pocos clientes. Esto indica que hay poca presencia de Olist en las pequeñas ciudades, casi todas las ventas son de las grandes  ciudades")
    st.markdown("---")
    
    st.subheader("Impacto, ¿Que puede hacer el negocio para mejorar?:")
    st.write("Con los resultados obtenidos podemos tomar dos decisiones:")
    st.write("- Centrarnos en las ciudades mas grandes, ya que hay se centran la mayoría de clientes.")
    st.write("- Explorar opciones de expansión en ciudades mas pequeñas, realizando por ejemplo campañas de publicidad.")
    st.markdown("---")
    
# Metodo que carga la pantalla con el analisis relacionado con los pedidos entre las diferentes ciudades y clientes
def pedidos_ciudades_clientes():
    st.title("📦 Pedidos y Clientes")
    st.write("En esta seccion se encuentra el análisis relacionado con los pedidos y clientes de la tienda.\n Existen campos modificables por el usuario para visualizar cambios en los gráficos en tiempo real.")
    st.markdown("---")

    st.subheader("Campos para modificar la información del gráfico:")
    # Sidebar con filtros
    top_n = st.slider("Selecciona el número de ciudades a mostrar", 5, 10, 20)

    criterio = st.selectbox("Ordenar ciudades por",
            options=['Numero Pedidos', 'Porcentaje Pedidos',
                     'Ratio Pedidos Cliente'],
            format_func=lambda x: {
                'Numero Pedidos': "Número de pedidos",
                'Porcentaje Pedidos': "Porcentaje de pedidos",
                'Ratio Pedidos Cliente': "Pedidos por cliente (ratio)"
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
    
    st.subheader("Análisis Descriptivo:")
    st.write("Sacamos unas conclusiones muy parecidas al punto anterior, hay poca presencia de Olist en pequeñas ciudades.\n Otro punto a destacar es que el ratio de pedidos por cliente es 1 en casi todas las ciudades, lo que indica una fidelidad prácticamente nula.")
    st.markdown("---")
    
    st.subheader("Impacto, ¿Que puede hacer el negocio para mejorar?:")
    st.write("Decisiones muy similares al punto anterior, y si de verdad ese es el ratio por cliente, se debería analizar porque pasa eso, ya que para una empresa la fidelización de los clientes es uno de los  aspectos mas importante:")
    st.markdown("---")

# Metodo que carga la pantalla con el analisis relacionado con los pedidos que han llegado con retraso
def pedidos_con_retraso():
    st.title("⏱️ Análisis de Pedidos con Retraso")
    st.write("En esta seccion se encuentra el análisis relacionado con los pedidos que cuentan con un retraso en su envío.")
    st.markdown("---")
    # Grafico de barras de numeros de clientes por estado
    st.subheader("Gráficos con datos relacionados a los retrasos de pedidos por ciudad:")
    # st.text("Este gráfico de barras muestra información relacionado con los pedidos en cada ciudad, puede mostrar diferente información dependiendo de lo seleccionado por el usuario anteriormente")
    graficos, df = vis_pedidos_con_retraso()
    for grafico in graficos:
        st.pyplot(grafico)
    st.markdown("---")
    
    # Tabla de numeros de clientes por ciudad
    st.subheader("Tabla con toda la información del análisis:")
    st.write(df)
    st.markdown("---")
    
    st.subheader("Análisis Descriptivo:")
    st.write("Comprobamos que el 97.55% de los retrasos se debe a problemas logísticos en el envio.")
    st.markdown("---")
    
    st.subheader("Impacto, ¿Que puede hacer el negocio para mejorar?:")
    st.write("Mediante conclusiones aproximadas en cálculos entre diferentes fechas, identificar porque pasan esos retrasos y explorar opciones de mejora:")
    st.markdown("---")

# Metrodo que carga la pantalla con el analisis de las opiniones de los clientes en base a los pedidos
def opiniones_pedidos():
    st.title("⭐ Opiniones de Clientes")
    st.write("En esta seccion se encuentra el análisis relacionado con las opiniones de los clientes.")
    st.markdown("---")
    
    # Subtítulo y descripción inicial
    st.subheader("Análisis geográfico de satisfacción del cliente")
    st.markdown(
        """
        Este mapa interactivo muestra la **puntuación media de reseñas por estado** en Brasil, 
        basado en las opiniones de los clientes que no han reportado retrasos. Cada estado está coloreado 
        según su nivel de satisfacción, lo que permite identificar rápidamente las regiones con mejor o 
        peor percepción del servicio. Consta con marcadores interactuables para mayor detalle.
        """
    )

    # Mapa generado
    pedidos_opiniones()

def metricas_adicionales():
    
    st.title("➕ Métricas Adicionales")
    st.markdown("---")
    st.subheader("Gráfico de barras Categorías Top por Estado:")
    st.text("Este gráfico muestra las categorías de producto con mayor volumen de ventas en el estado seleccionado, permitiendo identificar preferencias regionales de consumo.")
    estados = get_estados()
    
    estado = st.selectbox("Seleccionar Estado",
            options=estados,
        )
    fig = top_categorias(estado)    
    # Gráfico de barras de categorías más vendidas por estado
    
    st.pyplot(fig)
    st.markdown("---")
    
    st.subheader("Porcentaje de estados según su día de mayor venta")
    st.markdown(
        """
        Este gráfico muestra qué porcentaje de los estados tiene su mayor volumen de ventas en cada día de la semana.
        """
    )
    st.pyplot(dia_semana_mayor_ventas())

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
        inicio()

    elif seccion == "📍 Clientes, Estados y Ciudades":
        clientes_estados_ciudades()

    elif seccion == "📦 Pedidos, Ciudades y Clientes":
        pedidos_ciudades_clientes()

    elif seccion == "⏱️ Pedidos con Retraso":
        pedidos_con_retraso()

    elif seccion == "⭐ Opiniones (Reviews)":
        opiniones_pedidos()
        
    elif seccion == "➕ Métricas Adicionales":
        metricas_adicionales()


sidebar()
