
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

INPUT_FILE = RAW_DIR / "olist_customers_dataset.csv"
OUTPUT_FILE = PROCESSED_DIR / "customers_processed.csv"
FLAGS_FILE = PROCESSED_DIR / "customers_quality_flags.csv"

customers = pd.read_csv(
    INPUT_FILE,
    dtype={"customer_zip_code_prefix": "string"}
)

# Validate customer identifiers
customers["flag_missing_customer_id"] = (
    customers["customer_id"].isna()
    | customers["customer_id"].astype(str).str.strip().eq("")
)

customers["flag_missing_unique_id"] = (
    customers["customer_unique_id"].isna()
    | customers["customer_unique_id"].astype(str).str.strip().eq("")
)

# Validate ZIP codes
customers["flag_missing_zip_code"] = (
    customers["customer_zip_code_prefix"].isna()
)

customers["flag_invalid_zip_code"] = (
    ~customers["customer_zip_code_prefix"]
    .astype(str)
    .str.fullmatch(r"\d{5}", na=False)
)

# Validate city and state
customers["flag_missing_city"] = (
    customers["customer_city"].isna()
    | customers["customer_city"].astype(str).str.strip().eq("")
)

customers["flag_missing_state"] = (
    customers["customer_state"].isna()
    | customers["customer_state"].astype(str).str.strip().eq("")
)

# Save processed dataset
customers.to_csv(OUTPUT_FILE, index=False)

# Save records with quality issues
flag_columns = [
    column for column in customers.columns
    if column.startswith("flag_")
]

quality_flags = customers[
    customers[flag_columns].any(axis=1)
]

quality_flags.to_csv(FLAGS_FILE, index=False)

print("\n========== CUSTOMERS PROCESSING COMPLETE ==========")

print("Original rows:", len(customers))
print("Processed rows:", len(customers))
print("Flagged records:", len(quality_flags))

print("\nQuality flag counts:")

for column in flag_columns:
    print(f"{column}: {customers[column].sum()}")

print("\nGenerated files:")
print(OUTPUT_FILE)
print(FLAGS_FILE)

print("\nRaw dataset remains unchanged.")
