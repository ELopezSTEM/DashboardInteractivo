from src import data_loader

import pandas as pd

def data_cleaning():
	df_customer, df_orders = data_loader()

	#Cambio formato fechas
	df_orders["order_purchase_timestamp"] = pd.to_datetime(df_orders["order_purchase_timestamp"], errors="coerce")
	df_orders["order_approved_at"] = pd.to_datetime(df_orders["order_approved_at"], errors="coerce")
	df_orders["order_delivered_carrier_date"] = pd.to_datetime(df_orders["order_delivered_carrier_date"], errors="coerce")
	df_orders["order_delivered_customer_date"] = pd.to_datetime(df_orders["order_delivered_customer_date"], errors="coerce")
	df_orders["order_estimated_delivery_date"] = pd.to_datetime(df_orders["order_estimated_delivery_date"], errors="coerce")

	


	print(df_orders.head())
	return df_customer, df_orders
