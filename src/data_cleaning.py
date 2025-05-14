from src import data_loader

import pandas as pd

def data_cleaning():
	df_customer, df_orders, df_reviews = data_loader()

	#Cambio formato fechas
	df_orders["order_purchase_timestamp"] = pd.to_datetime(df_orders["order_purchase_timestamp"], errors="coerce")
	df_orders["order_approved_at"] = pd.to_datetime(df_orders["order_approved_at"], errors="coerce")
	df_orders["order_delivered_carrier_date"] = pd.to_datetime(df_orders["order_delivered_carrier_date"], errors="coerce")
	df_orders["order_delivered_customer_date"] = pd.to_datetime(df_orders["order_delivered_customer_date"], errors="coerce")
	df_orders["order_estimated_delivery_date"] = pd.to_datetime(df_orders["order_estimated_delivery_date"], errors="coerce")

	# Comprobación de valores nulos
	print("Valores nulos por columna:")
	print(df_orders.isnull().sum())
	print("\n")

	# Observamos que existen nulos en columnas importantes como:
	# 'order_approved_at', 'order_delivered_carrier_date' y 'order_delivered_customer_date'.
	# Vamos a analizar si estos valores nulos están justificados según el estado del pedido (order_status).

	#Analisis de 'order_approved_at'
	print("Analisis de nulos en 'order_approved_at' (Fecha de aprobacion):")
	nulos_approved = df_orders[df_orders["order_approved_at"].isnull()]
	grupo_approved = nulos_approved.groupby("order_status").size()
	print(grupo_approved, "\n")

	#Analisis de 'order_delivered_customer_date'
	print("Analisis de nulos en 'order_delivered_customer_date' (Fecha de entrega al cliente):")
	nulos_customer = df_orders[df_orders["order_delivered_customer_date"].isnull()]
	grupo_customer = nulos_customer.groupby("order_status").size()
	print(grupo_customer, "\n")

	#Analisis de 'order_delivered_carrier_date' ----
	print("Analisis de nulos en 'order_delivered_carrier_date' (Fecha de entrega al transportista):")
	nulos_carrier = df_orders[df_orders["order_delivered_carrier_date"].isnull()]
	grupo_carrier = nulos_carrier.groupby("order_status").size()
	print(grupo_carrier, "\n")

	#Conclusion:
	#La mayoría de los valores nulos en estas columnas se explican por el estado del pedido.
	#Por ejemplo, pedidos en estado 'created', 'canceled' o 'unavailable' no requieren fechas de aprobacion o entrega.
	#Solo se identifican algunos casos inconsistentes, como pedidos en estado 'delivered' sin fechas de entrega.
	#Como el porcentaje es muy bajo, no se consideramos necesario eliminar o imputar esos pedidos.

