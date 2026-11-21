
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

INPUT_FILE = RAW_DIR / "olist_orders_dataset.csv"
OUTPUT_FILE = PROCESSED_DIR / "orders_processed.csv"
FLAGS_FILE = PROCESSED_DIR / "orders_quality_flags.csv"

orders = pd.read_csv(INPUT_FILE)

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

# Missing timestamp flags
orders["flag_missing_approval"] = (
    orders["order_approved_at"].isna()
)

orders["flag_missing_carrier"] = (
    orders["order_delivered_carrier_date"].isna()
)

orders["flag_missing_delivery"] = (
    orders["order_delivered_customer_date"].isna()
)

# Invalid date sequence flags
orders["flag_carrier_before_purchase"] = (
    orders["order_delivered_carrier_date"]
    < orders["order_purchase_timestamp"]
)

orders["flag_delivery_before_purchase"] = (
    orders["order_delivered_customer_date"]
    < orders["order_purchase_timestamp"]
)

orders["flag_delivery_before_carrier"] = (
    orders["order_delivered_customer_date"]
    < orders["order_delivered_carrier_date"]
)

# Order status mismatch flags
orders["flag_delivered_missing_delivery"] = (
    (orders["order_status"] == "delivered")
    & orders["order_delivered_customer_date"].isna()
)

orders["flag_delivered_missing_carrier"] = (
    (orders["order_status"] == "delivered")
    & orders["order_delivered_carrier_date"].isna()
)

orders["flag_canceled_with_delivery"] = (
    (orders["order_status"] == "canceled")
    & orders["order_delivered_customer_date"].notna()
)

# Save processed dataset
orders.to_csv(OUTPUT_FILE, index=False)

# Save only records having at least one quality flag
flag_columns = [
    column for column in orders.columns
    if column.startswith("flag_")
]

quality_flags = orders[
    orders[flag_columns].any(axis=1)
]

quality_flags.to_csv(FLAGS_FILE, index=False)

print("\n========== ORDERS PROCESSING COMPLETE ==========")

print("Original rows:", len(orders))
print("Processed rows:", len(orders))
print("Flagged orders:", len(quality_flags))

print("\nQuality flag counts:")

for column in flag_columns:
    print(f"{column}: {orders[column].sum()}")

print("\nGenerated files:")
print(OUTPUT_FILE)
print(FLAGS_FILE)

print("\nRaw dataset remains unchanged.")
