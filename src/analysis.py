from src import data_cleaning

def analysis():
	df_customer, df_orders = data_cleaning()
	
	merged_data = df_customer.merge(df_orders, on="customer_id")

	clientes_por_estado = df_customer.groupby("customer_state")["customer_unique_id"].nunique()
