
import pandas as pd
from pathlib import Path

DATA = Path("data/raw")


def load(name):
    return pd.read_csv(DATA / name, dtype=str)


customers = load("olist_customers_dataset.csv")
orders = load("olist_orders_dataset.csv")
items = load("olist_order_items_dataset.csv")
products = load("olist_products_dataset.csv")
sellers = load("olist_sellers_dataset.csv")
payments = load("olist_order_payments_dataset.csv")
reviews = load("olist_order_reviews_dataset.csv")


# PRIMARY KEY VALIDATION

print("\nPRIMARY KEY VALIDATION")

primary_keys = {
    "customers": (customers, "customer_id"),
    "orders": (orders, "order_id"),
    "products": (products, "product_id"),
    "sellers": (sellers, "seller_id")
}

for table_name, (df, key) in primary_keys.items():
    duplicates = df[key].duplicated().sum()
    print(f"{table_name}: {len(df)} rows | {duplicates} duplicate keys")


# REVIEWS COMPOSITE KEY VALIDATION

print("\nREVIEWS COMPOSITE KEY VALIDATION")

review_duplicates = reviews.duplicated(
    subset=["review_id", "order_id"]
).sum()

print(
    f"reviews: {len(reviews)} rows | "
    f"{review_duplicates} duplicate composite keys"
)


# FOREIGN KEY VALIDATION

print("\nFOREIGN KEY VALIDATION")

checks = [
    ("Orders -> Customers", orders, "customer_id", customers, "customer_id"),
    ("Items -> Orders", items, "order_id", orders, "order_id"),
    ("Items -> Products", items, "product_id", products, "product_id"),
    ("Items -> Sellers", items, "seller_id", sellers, "seller_id"),
    ("Payments -> Orders", payments, "order_id", orders, "order_id"),
    ("Reviews -> Orders", reviews, "order_id", orders, "order_id")
]

for name, child, child_key, parent, parent_key in checks:
    orphan_count = (~child[child_key].isin(parent[parent_key])).sum()
    print(f"{name}: {orphan_count} orphan records")


print("\nRELATIONSHIP VALIDATION COMPLETED")
