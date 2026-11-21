
import pandas as pd
from pathlib import Path

DATA = Path("data/raw")

orders = pd.read_csv(DATA / "olist_orders_dataset.csv")

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )

print("\n========== DATE QUALITY CHECK ==========")

print("\nMissing timestamps:")

for column in date_columns:
    print(f"{column}: {orders[column].isna().sum()}")


print("\nInvalid date sequences:")

checks = {
    "Approval before purchase":
        orders["order_approved_at"] < orders["order_purchase_timestamp"],

    "Carrier dispatch before purchase":
        orders["order_delivered_carrier_date"] < orders["order_purchase_timestamp"],

    "Customer delivery before purchase":
        orders["order_delivered_customer_date"] < orders["order_purchase_timestamp"],

    "Customer delivery before carrier dispatch":
        orders["order_delivered_customer_date"] < orders["order_delivered_carrier_date"],

    "Estimated delivery before purchase":
        orders["order_estimated_delivery_date"] < orders["order_purchase_timestamp"]
}

for name, condition in checks.items():
    print(f"{name}: {condition.fillna(False).sum()}")


print("\n========== DATE QUALITY CHECK COMPLETED ==========")

print("\n========== INVALID DATE INVESTIGATION ==========")

invalid_carrier = orders[
    orders["order_delivered_carrier_date"]
    < orders["order_purchase_timestamp"]
]

print("\nCarrier before purchase:", len(invalid_carrier))

print(
    invalid_carrier[
        [
            "order_id",
            "order_status",
            "order_purchase_timestamp",
            "order_delivered_carrier_date",
            "order_delivered_customer_date"
        ]
    ].head(15).to_string(index=False)
)


invalid_delivery = orders[
    orders["order_delivered_customer_date"]
    < orders["order_delivered_carrier_date"]
]

print("\nCustomer delivery before carrier:", len(invalid_delivery))

print(
    invalid_delivery[
        [
            "order_id",
            "order_status",
            "order_purchase_timestamp",
            "order_delivered_carrier_date",
            "order_delivered_customer_date"
        ]
    ].to_string(index=False)
)


print("\nAffected order status distribution:")

print(
    pd.concat([invalid_carrier, invalid_delivery])[
        "order_status"
    ].value_counts()
)

print("\n========== ORDER STATUS VALIDATION ==========")

print("\nOrder status distribution:")
print(orders["order_status"].value_counts(dropna=False))


print("\nDelivered orders with missing delivery timestamp:")

delivered_missing = orders[
    (orders["order_status"] == "delivered")
    & (orders["order_delivered_customer_date"].isna())
]

print(len(delivered_missing))


print("\nDelivered orders with missing carrier timestamp:")

delivered_missing_carrier = orders[
    (orders["order_status"] == "delivered")
    & (orders["order_delivered_carrier_date"].isna())
]

print(len(delivered_missing_carrier))


print("\nCanceled orders with delivery timestamp:")

canceled_with_delivery = orders[
    (orders["order_status"] == "canceled")
    & (orders["order_delivered_customer_date"].notna())
]

print(len(canceled_with_delivery))


print("\n========== ORDER STATUS CHECK COMPLETED ==========")
print("\n========== STATUS MISMATCH INVESTIGATION ==========")

columns = [
    "order_id",
    "order_status",
    "order_purchase_timestamp",
    "order_delivered_carrier_date",
    "order_delivered_customer_date"
]

print("\n1. Delivered orders with missing delivery timestamp:")
print(delivered_missing[columns].to_string(index=False))

print("\n2. Delivered orders with missing carrier timestamp:")
print(delivered_missing_carrier[columns].to_string(index=False))

print("\n3. Canceled orders with delivery timestamp:")
print(canceled_with_delivery[columns].to_string(index=False))

print("\n========== INVESTIGATION COMPLETED ==========")