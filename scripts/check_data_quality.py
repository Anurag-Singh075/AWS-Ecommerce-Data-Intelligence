
import pandas as pd
from pathlib import Path

DATA = Path("data/raw")


def load(name):
    return pd.read_csv(DATA / name)


items = load("olist_order_items_dataset.csv")
payments = load("olist_order_payments_dataset.csv")
reviews = load("olist_order_reviews_dataset.csv")
products = load("olist_products_dataset.csv")


print("\n========== NUMERIC DATA QUALITY CHECK ==========")


# ORDER ITEMS VALIDATION

print("\nORDER ITEMS")

print("Invalid price:", (items["price"] <= 0).sum())
print("Negative freight value:", (items["freight_value"] < 0).sum())
print("Invalid order item number:", (items["order_item_id"] <= 0).sum())


# PAYMENTS VALIDATION

print("\nPAYMENTS")

print("Invalid payment value:", (payments["payment_value"] <= 0).sum())
print("Invalid payment installments:", (payments["payment_installments"] < 0).sum())


# REVIEWS VALIDATION

print("\nREVIEWS")

print("Invalid review scores:", (~reviews["review_score"].between(1, 5)).sum())


# PRODUCTS VALIDATION

print("\nPRODUCTS")

dimension_columns = [
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

for column in dimension_columns:
    invalid = (products[column].dropna() <= 0).sum()
    print(f"Invalid {column}: {invalid}")


print("\n========== NUMERIC QUALITY CHECK COMPLETED ==========")

print("\n========== INVALID PAYMENT INVESTIGATION ==========")

invalid_payments = payments[
    payments["payment_value"] <= 0
]

print("Invalid payment records:", len(invalid_payments))

print(
    invalid_payments[
        [
            "order_id",
            "payment_type",
            "payment_installments",
            "payment_value"
        ]
    ].to_string(index=False)
)


print("\n========== INVALID PRODUCT WEIGHT INVESTIGATION ==========")

invalid_weights = products[
    products["product_weight_g"] <= 0
]

print("Invalid product weight records:", len(invalid_weights))

print(
    invalid_weights[
        [
            "product_id",
            "product_category_name",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ]
    ].to_string(index=False)
)

print("\n========== ZERO PAYMENT ORDER INVESTIGATION ==========")

zero_payment_orders = invalid_payments["order_id"].unique()

related_payments = payments[
    payments["order_id"].isin(zero_payment_orders)
].sort_values(["order_id", "payment_value"])

print(
    related_payments[
        [
            "order_id",
            "payment_type",
            "payment_installments",
            "payment_value"
        ]
    ].to_string(index=False)
)

print("\nPayment summary for affected orders:")

print(
    related_payments.groupby("order_id").agg(
        payment_records=("payment_value", "count"),
        total_payment=("payment_value", "sum"),
        payment_types=("payment_type", lambda x: ", ".join(x))
    ).to_string()
)
