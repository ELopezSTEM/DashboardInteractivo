from src import data_loader

import pandas as pd

def data_cleaning():
	df_customer, df_orders, df_reviews, df_orders_items, df_products, df_translation = data_loader()

	# Cambio formato fechas
	df_orders["order_purchase_timestamp"] = pd.to_datetime(df_orders["order_purchase_timestamp"], errors="coerce")
	df_orders["order_approved_at"] = pd.to_datetime(df_orders["order_approved_at"], errors="coerce")
	df_orders["order_delivered_carrier_date"] = pd.to_datetime(df_orders["order_delivered_carrier_date"], errors="coerce")
	df_orders["order_delivered_customer_date"] = pd.to_datetime(df_orders["order_delivered_customer_date"], errors="coerce")
	df_orders["order_estimated_delivery_date"] = pd.to_datetime(df_orders["order_estimated_delivery_date"], errors="coerce")
	# Creamos una columna para el nombre del dia de la semana que realizo la compra
	df_orders["dia_semana"] = df_orders["order_purchase_timestamp"].dt.day_name()

	# Comprobación de valores nulos
	print("Valores nulos por columna:")
	print(df_orders.isnull().sum())
	print("\n")
	#Comprobamos los duplicados
	duplicados = df_orders.duplicated(keep=False).sum()
	print("Duplicados \"df_order:\"", duplicados)

	# Observamos que existen nulos en columnas importantes como:
	# 'order_approved_at', 'order_delivered_carrier_date' y 'order_delivered_customer_date'.
	# Vamos a analizar si estos valores nulos estan justificados segun el estado del pedido (order_status).

	# Analisis de 'order_approved_at'
	print("Analisis de nulos en 'order_approved_at' (Fecha de aprobacion):")
	nulos_approved = df_orders[df_orders["order_approved_at"].isnull()]
	grupo_approved = nulos_approved.groupby("order_status").size()
	print(grupo_approved, "\n")
	# Analisis de 'order_delivered_customer_date'
	print("Analisis de nulos en 'order_delivered_customer_date' (Fecha de entrega al cliente):")
	nulos_customer = df_orders[df_orders["order_delivered_customer_date"].isnull()]
	grupo_customer = nulos_customer.groupby("order_status").size()
	print(grupo_customer, "\n")
	# Analisis de 'order_delivered_carrier_date' 
	print("Analisis de nulos en 'order_delivered_carrier_date' (Fecha de entrega al transportista):")
	nulos_carrier = df_orders[df_orders["order_delivered_carrier_date"].isnull()]
	grupo_carrier = nulos_carrier.groupby("order_status").size()
	print(grupo_carrier, "\n")
	# Conclusion:
	#   La mayoria de los valores nulos en estas columnas se explican por el estado del pedido.
	#   Por ejemplo, pedidos en estado 'created', 'canceled' o 'unavailable' no requieren fechas de aprobacion o entrega.
	#   Solo se identifican algunos casos inconsistentes, como pedidos en estado 'delivered' sin fechas de entrega.
	#   Como el porcentaje es muy bajo, no se consideramos necesario eliminar o imputar esos pedidos.

	#Otros duplicados a comprobar
	duplicados = df_reviews.duplicated(keep=False).sum()
	print("Duplicados \"df_reviews:\"", duplicados)

	duplicados = df_customer.duplicated(keep=False).sum()
	print("Duplicados \"df_customer:\"", duplicados)
	# No encontramos duplicados

	# Limpiza categorias
	df_products_limpio = df_products.merge(df_translation, on = "product_category_name", how = "left")
	df_products_limpio["product_category_name_english"] = df_products_limpio["product_category_name_english"].fillna("Unknown")

	df_products_limpio = df_products_limpio.drop(columns = ["product_category_name"])
	df_products_limpio = df_products_limpio.rename(columns = {"product_category_name_english" : "product_category_name"})

	return df_customer, df_orders, df_reviews, df_orders_items, df_products_limpio