# Importaciones librerias
import matplotlib.pyplot as plt

# Importaciones metodos de analisis
from .analysis import top_5_estados
from .analysis import tabla_metricas_pedidos
from .analysis import analisis_retrasos

# Grafico de barras que muestra estados y numero de clientes por cada uno.
def clientes_estado(fecha_inicio, fecha_fin):
    
    # DataFrame recibido desde el analisis.
    df = top_5_estados(fecha_inicio, fecha_fin)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Color
    color = "#4C72B0"
    
    # Barra
    bars = ax.bar(df['customer_state'], df['customer_sum'], color=color)

    # Título
    ax.set_title("Clientes por Estado", fontsize=16, pad=20)

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
    if criterio not in ['num_pedidos', 'porcentaje_pedidos', 'ratio_pedidos_cliente']:
        raise ValueError("El criterio debe ser 'num_pedidos', 'porcentaje_pedidos' o 'ratio_pedidos_cliente'.")

    # Seleccionar top ciudades ordenados por el criterio seleccionado y cantidad seleccionada
    top_ciudades = df.sort_values(by=criterio, ascending=False).head(num_ciudades)

    # Crear figura
    fig, ax = plt.subplots(figsize=(10, 6))

    # Gráfico de barras horizontal
    ax.barh(top_ciudades['customer_city'], top_ciudades[criterio], color='#1f77b4')
    ax.invert_yaxis()  # Ciudades con mayor valor arriba

    # Etiquetas
    ax.set_xlabel(criterio.replace('_', ' ').capitalize())
    ax.set_title(f"Top {num_ciudades} ciudades por {criterio.replace('_', ' ')}")
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    # Etiquetas de valor al lado de cada barra
    for i, (valor, ciudad) in enumerate(zip(top_ciudades[criterio], top_ciudades['customer_city'])):
        ax.text(valor, i, f"{valor:.2f}" if isinstance(valor, float) else str(valor),
                va='center', ha='left', fontsize=9, color='black')

    # Espacio limpio alrededor del gráfico
    plt.tight_layout()
    return fig, df

def pedidos_con_retraso():
    
    df = analisis_retrasos()
    
    print(df)
    
    
