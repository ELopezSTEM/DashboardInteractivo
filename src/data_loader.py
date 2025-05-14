import pandas as pd

def data_loader():
	try:
		df_customer = pd.read_csv("data/raw/olist_customers_dataset.csv")
		df_orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
		df_reviews = pd.read_csv("data/raw/olist_order_reviews_dataset.csv")
		df_orders_items = pd.read_csv("data/raw/olist_order_items_dataset.csv")
		df_products = pd.read_csv("data/raw/olist_products_dataset.csv")
		df_translation = pd.read_csv("data/raw/product_category_name_translation.csv")
		return df_customer, df_orders, df_reviews, df_orders_items, df_products, df_translation
	except FileNotFoundError as e:
		print(f"File {e} not found.")
		return None, None, None, None, None, None