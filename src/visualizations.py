import matplotlib.pyplot as plt
import pandas as pd

from .analysis import top_5_estados

def grafico_barras_estados(fecha_inicio, fecha_fin):
    
    df = top_5_estados(fecha_inicio, fecha_fin)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Color sobrio
    color = "#4C72B0"  # azul elegante
    bars = ax.bar(df['customer_state'], df['customer_sum'], color=color)

    # Título elegante
    ax.set_title("Clientes por Estado", fontsize=16, pad=20)

    # Ejes limpios
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_alpha(0.2)
    ax.spines['bottom'].set_alpha(0.2)

    # Etiquetas del eje Y
    ax.set_ylabel("Nº de Clientes", fontsize=13)
    ax.tick_params(axis='y', labelsize=11)
    ax.tick_params(axis='x', labelsize=11, rotation=45)

    # Quitar líneas de los ticks
    ax.tick_params(axis='both', length=0)

    # Añadir valores encima de las barras
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