from src import data_cleaning
import pandas as pd


df_customer, df_orders, df_reviews, df_orders_items, df_products_limpio = data_cleaning()
merged_data = df_customer.merge(df_orders, on="customer_id")


# ----------------- EJERCICIO 1 ----------------- 
# Calcula el top 5 de estados con mas CLIENTES UNICOS en un rango de fechas.
# Se filtra por 'order_purchase_timestamp' para centrarse en pedidos realizados en ese periodo.
# Se usa 'customer_unique_id' para contar clientes reales (no repetir por pedido).
# Devuelve un DataFrame con columnas:
#   -"Estado"
#   -"Numero Clientes"
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

# Devuelve el numero de clientes unicos por ciudad y estado en un periodo dado.
# Filtra por fecha de compra y agrupa por ciudad y estado.
# Usa 'customer_unique_id' para contar solo una vez a cada cliente.
# Devuelve un DataFrame con columnas:
#   -"Ciudad" (indice)
#   -"Estado"
#   -"Numero Clientes"
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


# ----------------- EJERCICIO 2 ----------------- 
# Calcula metricas de clientes y pedidos por ciudad y estado en un periodo.
# Se agrupa por ciudad y estado para obtener num. de clientes unicos, num. de pedidos, % sobre el total y el ratio pedidos por cliente.
# Devuelve un DataFrame con columnas:
#   -"Ciudad" (iindice)
#   -"Estado"
#   -"Numero Clientes"
#   -"Numero Pedidos"
#   -"Porcentaje Pedidos"
#   -"Ratio Pedidos Clente"
def tabla_metricas_pedidos():

    
    resumen_ciudades = merged_data.groupby(
        ["customer_city", "customer_state"]
    )["customer_unique_id"].nunique().reset_index(name = "num_clientes")

    pedidos_ciudad_estado = merged_data.groupby(
        ["customer_city", "customer_state"]
    )["order_id"].nunique().reset_index(name = "num_pedidos")
    
    tabla_final = resumen_ciudades.merge(pedidos_ciudad_estado, on = ["customer_state", "customer_city"])
    
    total_pedidos = tabla_final["num_pedidos"].sum()
    
    tabla_final["porcentaje_pedidos"] = (tabla_final["num_pedidos"] / total_pedidos) * 100
    tabla_final["ratio_pedidos_cliente"] = tabla_final["num_pedidos"] / tabla_final["num_clientes"]
    
    
    tabla_final.columns = ["Ciudad", "Estado", "Numero Clientes", "Numero Pedidos", "Porcentaje Pedidos", "Ratio Pedidos Cliente"]
    tabla_final = tabla_final.set_index("Ciudad")
    
    return tabla_final


# ----------------- EJERCICIO 3 ----------------- 
# Diagnostico rapido sobre posibles causas del retraso
def diagnostico(row):
    if row["retraso_medio_dias"] <= 0:
        return "Sin retraso"
    
    if row["tiempo_medio_preparacion"] > row["tiempo_medio_envio"]:
        return "Retraso causado por el vendedor (preparacion lenta)"
    
    if row["tiempo_medio_envio"] > row["tiempo_medio_preparacion"]:
        return "Retraso causado por la logistica (envio lento)"
    
    if row["tiempo_medio_aprobacion"] > 2:
        return "Retraso por aprobacion de pago lenta"
    
    return "Retraso indeterminado"

# Muestra las ciudades con pedidos que llegaron tarde, el % de retrasos y el retraso medio en dias.
# Se calcula la diferencia entre fecha de entrega real y estimada, y se filtran los pedidos con retraso.
# Devuelve un DataFrame con columnas:
#   -"Ciudad" (indice)
#   -"Total Pedidos"
#   -"Pedidos Retrasados"
#   -"Retraso Medio Dias"
#   -"Porcentaje Retrasados"
#   -"Diagnostico"
def analisis_retrasos():
    df_filtrado = merged_data.copy()
    
    df_filtrado["tiempo_aprobacion"] = (df_filtrado["order_approved_at"] - df_filtrado["order_purchase_timestamp"]).dt.days
    df_filtrado["tiempo_preparacion"] = (df_filtrado["order_delivered_carrier_date"] - df_filtrado["order_approved_at"]).dt.days
    df_filtrado["tiempo_envio"] = (df_filtrado["order_delivered_customer_date"] - df_filtrado["order_delivered_carrier_date"]).dt.days
    df_filtrado["retraso_dias"] = (df_filtrado["order_delivered_customer_date"] - df_filtrado["order_estimated_delivery_date"]).dt.days

    retrasos = df_filtrado[df_filtrado["retraso_dias"] > 0]

    total_pedidos_ciudad = df_filtrado.groupby("customer_city")["order_id"].count().reset_index(name="total_pedidos")

    retrasos_ciudad = retrasos.groupby("customer_city").agg(
        pedidos_retrasados=("order_id", "count"),
        retraso_medio_dias=("retraso_dias", "mean"),
        tiempo_medio_aprobacion=("tiempo_aprobacion", "mean"),
        tiempo_medio_preparacion=("tiempo_preparacion", "mean"),
        tiempo_medio_envio=("tiempo_envio", "mean")
    ).reset_index()

    tabla_retrasos = total_pedidos_ciudad.merge(retrasos_ciudad, on="customer_city", how="left").fillna(0)

    tabla_retrasos["porcentaje_retrasados"] = (
        tabla_retrasos["pedidos_retrasados"] / tabla_retrasos["total_pedidos"]
    ) * 100

    tabla_retrasos["diagnostico"] = tabla_retrasos.apply(diagnostico, axis=1)

    # Limpiar columnas técnicas
    tabla_retrasos = tabla_retrasos.drop(columns=[
        "tiempo_medio_aprobacion", "tiempo_medio_preparacion", "tiempo_medio_envio"
    ])

    # Renombrado y filtrado final
    tabla_retrasos.columns = [
        "Ciudad", "Total Pedidos", "Pedidos Retrasados",
        "Retraso Medio Dias", "Porcentaje Retrasados", "Diagnostico"
    ]
    tabla_retrasos = tabla_retrasos.set_index("Ciudad")
    tabla_retrasos = tabla_retrasos[tabla_retrasos["Pedidos Retrasados"] > 0]

    return tabla_retrasos


# ----------------- EJERCICIO 4 ----------------- 
# Calcula cuantas reviews tiene cada estado y su puntuacion media, excluyendo los pedidos que llegaron tarde.
# Se filtra 'merged_data' para quitar pedidos con retraso y luego se cruza con las reviews.
# Devuelve un DataFrame con columnas:
#   -"Estado" ('ndice)
#   -"Numero_Reviews"
#   -"Score_Medio"
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


# ------------------PARTE NO OBLIGATORIA------------------


# Calcula el top 5 de categorias mas vendidas en un estado concreto.
# Une pedidos, clientes, productos y ventas, filtra por estado y cuenta ventas por categoria.
# Devuelve un DataFrame con columnas:
#   -"Categoria" (indice)
#   -"Total de Ventas"
def top_categoria(estado):
    merged_op1 = df_orders.merge(df_customer, on = "customer_id")
    merged_op1 = merged_op1.merge(df_orders_items, on = "order_id")
    merged_op1 = merged_op1.merge(df_products_limpio, on = "product_id")
    
    merged_estado = merged_op1[merged_op1["customer_state"] == estado]
    
    categoria_ventas = merged_estado.groupby("product_category_name").agg(
        total_ventas = ("order_id", "count")
    ).reset_index()
    
    top_5 = categoria_ventas.sort_values("total_ventas", ascending = False).head(5)
    top_5.columns = ["Categoria", "Total de Ventas"]
    top_5 = top_5.set_index("Categoria")
    
    return top_5


# Analiza el dia de la semana con mas ventas por estado y a nivel nacional.
# Agrupa por estado y dia, identifica el top por estado, calcula que porcentaje de estados tiene cada dia como top,
# y también obtiene el dia con mas ventas en todo el pais.
# Return 1 → DataFrame con columnas:
#   -"Estado" (indice)
#  -"Dia Semana"
#  -"Total_Pedidos"
# Return 2 → DataFrame con columnas:
#   -"Dia Semana" (indice)
#   -"Porcentaje Estados"
# Return 3 → String con el nombre del dia de la semana con mas ventas a nivel nacional
def analisis_dia_semana():
    dias = merged_data.groupby(["customer_state", "dia_semana"]).agg(
        total_pedidos = ("order_id", "count")
    ).reset_index()
    
    dia_top_estado = dias.sort_values("total_pedidos", ascending = False)
    dia_top_estado = dia_top_estado.groupby("customer_state").first().reset_index()
    
    porcentaje_dias = dia_top_estado["dia_semana"].value_counts(normalize = False).reset_index()
    porcentaje_dias.columns = ["dia_semana", "num_estados"]
    
    total_estados = dia_top_estado["customer_state"].nunique()
    porcentaje_dias["porcentaje_estados"] = round((porcentaje_dias["num_estados"] / total_estados * 100), 2)
    
    dia_top_estado.columns = ["Estado", "Dia Semana", "Total_Pedidos"]
    dia_top_estado = dia_top_estado.set_index("Estado")
    
    porcentaje_dias = porcentaje_dias.drop(columns = ["num_estados"])
    porcentaje_dias.columns = ["Dia Semana", "Porcentaje Estados"]
    porcentaje_dias =porcentaje_dias.set_index("Dia Semana")
    
    dia_top_nacional = merged_data["dia_semana"].value_counts().idxmax()
    
    return dia_top_estado, porcentaje_dias, dia_top_nacional

def get_estados():
    return merged_data.groupby("customer_state")