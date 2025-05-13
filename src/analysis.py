from src import data_cleaning
import pandas as pd


df_customer, df_orders = data_cleaning()
merged_data = df_customer.merge(df_orders, on="customer_id")


def top_5_estados(fecha_inicio, fecha_fin):

    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    df_filtrado = merged_data[
        (df_orders["order_purchase_timestamp"] >= fecha_inicio) &
        (df_orders["order_purchase_timestamp"] <= fecha_fin)
    ]

    clientes_por_estado = df_filtrado.groupby(
        "customer_state")["customer_unique_id"].nunique().reset_index()
    clientes_por_estado.columns = ["customer_state", "customer_sum"]

    top_5 = clientes_por_estado.sort_values(
        by="customer_sum", ascending=False).head(5)

    return top_5


def tabla_ciudades(fecha_inicio, fecha_fin):

    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    df_filtrado = merged_data[
        (merged_data["order_purchase_timestamp"] >= fecha_inicio) &
        (merged_data["order_purchase_timestamp"] <= fecha_fin)
    ]

    resumen_ciudades = df_filtrado.groupby(
        ["customer_city", "customer_state"]
    )["customer_unique_id"].nunique().reset_index()

    resumen_ciudades.columns = ["Ciudad", "Estado", "Numero Clientes"]
    resumen_ciudades = resumen_ciudades.set_index("Ciudad")

    return resumen_ciudades
