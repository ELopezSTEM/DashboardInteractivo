from src import data_cleaning
import pandas as pd


df_customer, df_orders, df_reviews = data_cleaning()
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
    clientes_por_estado.columns = ["Estado", "Numero Clientes"]

    top_5 = clientes_por_estado.sort_values(
        by="Numero Clientes", ascending=False).head(5)

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

def tabla_metricas_pedidos(fecha_inicio, fecha_fin):
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    df_filtrado = merged_data[
        (merged_data["order_purchase_timestamp"] >= fecha_inicio) &
        (merged_data["order_purchase_timestamp"] <= fecha_fin)]
    
    resumen_ciudades = df_filtrado.groupby(
        ["customer_city", "customer_state"]
    )["customer_unique_id"].nunique().reset_index(name = "num_clientes")

    pedidos_ciudad_estado = df_filtrado.groupby(
        ["customer_city", "customer_state"]
    )["order_id"].nunique().reset_index(name = "num_pedidos")
    
    tabla_final = resumen_ciudades.merge(pedidos_ciudad_estado, on = ["customer_state", "customer_city"])
    
    total_pedidos = tabla_final["num_pedidos"].sum()
    
    tabla_final["porcentaje_pedidos"] = (tabla_final["num_pedidos"] / total_pedidos) * 100
    tabla_final["ratio_pedidos_cliente"] = tabla_final["num_pedidos"] / tabla_final["num_clientes"]
    
    
    tabla_final.columns = ["Ciudad", "Estado", "Numero Clientes", "Numero Pedidos", "Porcentaje Pedidos", "Ratio Pedidos Cliente"]
    tabla_final = tabla_final.set_index("Ciudad")
    
    return tabla_final
    
def analisis_retrasos():
    df_filtrado = merged_data.copy()
    
    df_filtrado["retraso_dias"] = (df_filtrado["order_delivered_customer_date"] - df_filtrado["order_estimated_delivery_date"]).dt.days

    retrasos = df_filtrado[df_filtrado["retraso_dias"] > 0]

    total_pedidos_ciudad = df_filtrado.groupby("customer_city")["order_id"].count().reset_index(name="total_pedidos")

    retrasos_ciudad = retrasos.groupby("customer_city").agg(
        pedidos_retrasados=("order_id", "count"),
        retraso_medio_dias=("retraso_dias", "mean")
    ).reset_index()

    tabla_retrasos = total_pedidos_ciudad.merge(retrasos_ciudad, on="customer_city", how="left").fillna(0)

    tabla_retrasos["porcentaje_retrasados"] = (tabla_retrasos["pedidos_retrasados"] / tabla_retrasos["total_pedidos"]) * 100


    tabla_retrasos.columns = ["Ciudad", "Total Pedidos", "Pedidos Retrasados", "Retraso Medio Dias", "Porcentaje Retrasados"]
    tabla_retrasos = tabla_retrasos.set_index("Ciudad")
    
    tabla_retrasos = tabla_retrasos[tabla_retrasos["Pedidos Retrasados"] > 0]

    return tabla_retrasos

def analisis_reviews_sin_retrasos():
    
    df_filtrado = merged_data.copy()
    
    df_filtrado["retraso_dias"] = (
        df_filtrado["order_delivered_customer_date"] - df_filtrado["order_estimated_delivery_date"]
    ).dt.days

    df_sin_retraso = df_filtrado[df_filtrado["retraso_dias"] <= 0]

    df_reviews_filtrado = df_reviews.merge(
        df_sin_retraso[["order_id", "customer_state"]],
        on="order_id", how="inner"
    )
    
    resumen_reviews = df_reviews_filtrado.groupby("customer_state").agg(
        num_reviews = ("review_id", "count"),
        score_medio = ("review_score", "mean")
	).reset_index()
    
    resumen_reviews.columns = ["Estado", "Numero_Reviews", "Score_Medio"]
    resumen_reviews = resumen_reviews.set_index("Estado")
    
    return resumen_reviews