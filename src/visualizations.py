# Importaciones librerias
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import streamlit as st
from shapely.geometry import Point

# Importaciones metodos de analisis
from .analysis import top_5_estados
from .analysis import tabla_metricas_pedidos
from .analysis import analisis_retrasos
from .analysis import analisis_reviews_sin_retrasos
from .analysis import top_categoria
from .analysis import analisis_dia_semana


# Grafico de barras que muestra estados y numero de clientes por cada uno.
def clientes_estado(fecha_inicio, fecha_fin):
    
    # DataFrame recibido desde el analisis.
    df = top_5_estados(fecha_inicio, fecha_fin)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Color
    color = "#4C72B0"
    
    # Barra
    bars = ax.bar(df['Estado'], df['Numero Clientes'], color=color)

    # Título
    ax.set_title("Nª Clientes por Estado", fontsize=16, pad=20)

    # Ejes limpios
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_alpha(0.2)
    ax.spines['bottom'].set_alpha(0.2)

    ax.tick_params(axis='y', labelsize=11)
    ax.tick_params(axis='x', labelsize=11, rotation=45)

    # Quitar líneas de los ticks
    ax.tick_params(axis='both', length=0)

    # Añadir valores exactos encima de las barras
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),  # Desplazamiento vertical
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=11, color='#333333')

    # Espacio limpio alrededor del gráfico
    fig.tight_layout()
    return fig

# Grafico de barras que muestra informacion de los pedidos de los clientes por ciudad.
def pedidos_por_ciudad(num_ciudades, criterio):
    df = tabla_metricas_pedidos()
    
    # Validar criterio
    if criterio not in ['Numero Pedidos', 'Porcentaje Pedidos', 'Ratio Pedidos Cliente']:
        raise ValueError("El criterio debe ser 'num_pedidos', 'porcentaje_pedidos' o 'ratio_pedidos_cliente'.")

    # Seleccionar top ciudades ordenados por el criterio seleccionado y cantidad seleccionada
    top_ciudades = df.sort_values(by=criterio, ascending=False).head(num_ciudades)

    # Crear figura
    fig, ax = plt.subplots(figsize=(10, 6))

    # Gráfico de barras horizontal
    ax.barh(top_ciudades.index, top_ciudades[criterio], color='#1f77b4')
    ax.invert_yaxis()  # Ciudades con mayor valor arriba

    # Etiquetas
    ax.set_xlabel(criterio.replace('_', ' ').capitalize())
    ax.set_title(f"Top {num_ciudades} ciudades por {criterio.replace('_', ' ')}")
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    # Etiquetas de valor al lado de cada barra
    for i, (valor, ciudad) in enumerate(zip(top_ciudades[criterio], top_ciudades.index)):
        ax.text(valor, i, f"{valor:.2f}" if isinstance(valor, float) else str(valor),
                va='center', ha='left', fontsize=9, color='black')

    # Espacio limpio alrededor del gráfico
    plt.tight_layout()
    return fig, df

def pedidos_con_retraso():
    
    df = analisis_retrasos()
    
    df_ordenado = df.sort_values(by="Pedidos Retrasados", ascending=False).head(10)
    
    metricas = [
        ('Pedidos Retrasados', 'Pedidos retrasados', 'crimson'),
        ('Porcentaje Retrasados', '% de pedidos retrasados', 'darkorange'),
        ('Retraso Medio Dias', 'Retraso medio en días', 'steelblue')
    ]

    figuras = []

    for col, titulo, color in metricas:
        fig, ax = plt.subplots(figsize=(8, 4))
        
        bars = ax.barh(df_ordenado.index, df_ordenado[col], color=color)
        ax.set_title(titulo, fontsize=13)
        ax.set_xlabel('Valor')
        ax.grid(True, axis='y', linestyle='--', alpha=0.5)

        fig.tight_layout()
        figuras.append(fig)
        
    return figuras, df
    
    
def get_star_rating(score):
    """Convierte la puntuación en estrellas (de 1 a 5) con emojis."""
    stars = int(round(score))  # redondea al entero más cercano
    return '⭐' * stars + '☆' * (5 - stars)

@st.cache_resource
def pedidos_opiniones():
    # 1. Cargar datos de reviews sin retrasos
    df_reviews = analisis_reviews_sin_retrasos()

    # 2. Cargar GeoJSON de estados de Brasil
    url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/main/public/data/brazil-states.geojson"
    gdf_brasil = gpd.read_file(url)

    # 3. Asegurarse de que las columnas coincidan y eliminar columnas innecesarias
    gdf_brasil = gdf_brasil.rename(columns={"sigla": "Estado"})  # Asegura coincidencia
    gdf_merged = gdf_brasil.merge(df_reviews, on="Estado", how="left")
    gdf_merged = gdf_merged.drop(columns=["created_at", "updated_at"], errors="ignore")

    # 4. Crear el mapa base bloqueado (sin zoom ni arrastre)
    m = folium.Map(
        location=[-14.2350, -51.9253],
        zoom_start=4,
        tiles='cartodb positron',
        zoom_control=False,
        dragging=False,
        scrollWheelZoom=False,
        doubleClickZoom=False,
        touchZoom=False
    )

    # 5. Convertir a GeoJSON sin columnas problemáticas
    geojson_data = gdf_merged.to_json()
    
    # Obtener valores mínimo y máximo reales
    min_score = gdf_merged['Score_Medio'].min()
    max_score = gdf_merged['Score_Medio'].max()

    # Asegurarse de que el máximo sea un poco más alto para incluir el valor superior
    if max_score == min_score:
        # Todos los valores son iguales; evita error
        threshold_scale = [min_score, min_score + 0.01]
    else:
        threshold_scale = list(np.linspace(min_score, max_score, 6)) 

    # 6. Añadir Choropleth (colores por score)
    folium.Choropleth(
        geo_data=geojson_data,
        name='choropleth',
        data=gdf_merged,
        columns=['Estado', 'Score_Medio'],
        key_on='feature.properties.Estado',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Media de puntos en las reseñas',
        threshold_scale=threshold_scale,
        bins=None, 
        reset=True
    ).add_to(m)

    for _, row in gdf_merged.iterrows():
        if not row['geometry'].is_empty:
            # Obtener centroide del polígono
            centroid = row['geometry'].centroid

            # Obtener estrellas
            star_rating = get_star_rating(row['Score_Medio'])

            # Crear contenido HTML personalizado
            popup_html = f"""
            <div style="font-family: Arial; font-size: 14px;">
                <h4 style="margin-bottom: 5px; color: #2A6599;">{row['Estado']}</h4>
                <p style="margin: 0;"><b>Puntuación Media:</b><br> {row['Score_Medio']:.2f}</p>
                <p style="margin: 0;">{star_rating}</p>
                <p style="margin: 0;"><b>Reseñas totales:</b><br> {row['Numero_Reviews']}</p>
            </div>
            """

            # Crear el marcador
            folium.Marker(
                location=[centroid.y, centroid.x],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)


    return st_folium(m, width=725)
    

def top_categorias(estado):
    df = top_categoria(estado)
    
    fig, ax = plt.subplots(figsize=(10, 6))

    # Color
    color = "#4C72B0"
    
    # Barra
    bars = ax.bar(df.index, df['Total de Ventas'], color=color)

    # Título
    ax.set_title("Mejores Categorias de Producto por Estado", fontsize=16, pad=20)

    # Ejes limpios
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_alpha(0.2)
    ax.spines['bottom'].set_alpha(0.2)

    ax.tick_params(axis='y', labelsize=11)
    ax.tick_params(axis='x', labelsize=11, rotation=45)

    # Quitar líneas de los ticks
    ax.tick_params(axis='both', length=0)

    # Añadir valores exactos encima de las barras
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),  # Desplazamiento vertical
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=11, color='#333333')

    # Espacio limpio alrededor del gráfico
    fig.tight_layout()
    return fig
    
    
def dia_semana_mayor_ventas():
    df, df2, string = analisis_dia_semana()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    df2['Porcentaje Estados'].plot(kind='line', marker='o', ax=ax, color='blue')

    ax.set_title("(%) de Estados por Día de la Semana", fontsize=14)
    ax.set_ylabel("Porcentaje de Estados(%)")
    ax.set_xlabel("Día de la Semana")
    ax.grid(True)
    plt.xticks(rotation=45)
    return fig
    
    
