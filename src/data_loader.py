import pandas as pd

def data_loader():
	try:
		df_customer = pd.read_csv("data/raw/olist_customers_dataset.csv")
		df_orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
		df_reviews = pd.read_csv("data/raw/olist_order_reviews_dataset.csv")
		return df_customer, df_orders, df_reviews
	except FileNotFoundError as e:
		print(f"File {e} not found.")
		return None, None