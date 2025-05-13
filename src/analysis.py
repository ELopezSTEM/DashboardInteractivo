from src import data_cleaning


df_customer, df_orders = data_cleaning()
merged_data = df_customer.merge(df_orders, on="customer_id")

def top_5_estados(fecha_inicio, fecha_fin):

	df_filtrado = merged_data[
		(df_orders["order_purchase_timestamp"] >= fecha_inicio) &
		(df_orders["order_purchase_timestamp"] <= fecha_fin)
	]

	clientes_por_estado = df_filtrado.groupby("customer_state")["customer_unique_id"].nunique()
	clientes_por_estado.columns = ["customer_state", "customer_sum"]

	top_5 = clientes_por_estado.sort_values(ascending=False).max(5)

	return top_5
