
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def save_outputs(name, df):
    flag_columns = [
        col for col in df.columns
        if col.startswith("flag_")
    ]

    output_file = PROCESSED_DIR / f"{name}_processed.csv"
    flags_file = PROCESSED_DIR / f"{name}_quality_flags.csv"

    df.to_csv(output_file, index=False)

    quality_flags = df[df[flag_columns].any(axis=1)]
    quality_flags.to_csv(flags_file, index=False)

    print(f"\n{name.upper()} PROCESSING")
    print("Original rows:", len(df))
    print("Processed rows:", len(df))
    print("Flagged records:", len(quality_flags))

    for col in flag_columns:
        print(f"{col}: {df[col].sum()}")

    print("Saved:", output_file)
    print("Saved:", flags_file)


def load_csv(filename, **kwargs):
    return pd.read_csv(RAW_DIR / filename, **kwargs)


# ==========================================
# 1. PRODUCTS
# ==========================================

products = load_csv("olist_products_dataset.csv")

products["flag_missing_product_id"] = products["product_id"].isna()
products["flag_missing_category"] = products["product_category_name"].isna()

numeric_product_columns = [
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
    "product_photos_qty"
]

for col in numeric_product_columns:
    products[col] = pd.to_numeric(products[col], errors="coerce")

products["flag_missing_weight"] = products["product_weight_g"].isna()
products["flag_invalid_weight"] = products["product_weight_g"].le(0)

products["flag_missing_dimensions"] = products[
    ["product_length_cm", "product_height_cm", "product_width_cm"]
].isna().any(axis=1)

products["flag_invalid_dimensions"] = products[
    ["product_length_cm", "product_height_cm", "product_width_cm"]
].le(0).any(axis=1)

save_outputs("products", products)


# ==========================================
# 2. SELLERS
# ==========================================

sellers = load_csv(
    "olist_sellers_dataset.csv",
    dtype={"seller_zip_code_prefix": "string"}
)

sellers["flag_missing_seller_id"] = sellers["seller_id"].isna()

sellers["flag_missing_zip"] = (
    sellers["seller_zip_code_prefix"].isna()
)

sellers["flag_invalid_zip"] = (
    ~sellers["seller_zip_code_prefix"]
    .str.fullmatch(r"\d{5}", na=False)
)

sellers["flag_missing_city"] = sellers["seller_city"].isna()
sellers["flag_missing_state"] = sellers["seller_state"].isna()

save_outputs("sellers", sellers)


# ==========================================
# 3. PAYMENTS
# ==========================================

payments = load_csv("olist_order_payments_dataset.csv")

payments["payment_value"] = pd.to_numeric(
    payments["payment_value"], errors="coerce"
)

payments["payment_installments"] = pd.to_numeric(
    payments["payment_installments"], errors="coerce"
)

payments["flag_missing_order_id"] = payments["order_id"].isna()
payments["flag_invalid_payment_value"] = (
    payments["payment_value"].le(0)
    | payments["payment_value"].isna()
)

payments["flag_invalid_installments"] = (
    payments["payment_installments"].lt(0)
    | payments["payment_installments"].isna()
)

save_outputs("payments", payments)


# ==========================================
# 4. REVIEWS
# ==========================================

reviews = load_csv("olist_order_reviews_dataset.csv")

reviews["review_score"] = pd.to_numeric(
    reviews["review_score"], errors="coerce"
)

reviews["flag_missing_review_id"] = reviews["review_id"].isna()
reviews["flag_missing_order_id"] = reviews["order_id"].isna()

reviews["flag_invalid_review_score"] = (
    ~reviews["review_score"].between(1, 5)
)

# Empty review comments are optional, not automatically invalid.

save_outputs("reviews", reviews)


# ==========================================
# 5. ORDER ITEMS
# ==========================================

items = load_csv("olist_order_items_dataset.csv")

for col in ["order_item_id", "price", "freight_value"]:
    items[col] = pd.to_numeric(items[col], errors="coerce")

items["flag_missing_order_id"] = items["order_id"].isna()
items["flag_missing_product_id"] = items["product_id"].isna()
items["flag_missing_seller_id"] = items["seller_id"].isna()

items["flag_invalid_item_number"] = (
    items["order_item_id"].le(0)
    | items["order_item_id"].isna()
)

items["flag_invalid_price"] = (
    items["price"].le(0) | items["price"].isna()
)

items["flag_invalid_freight"] = (
    items["freight_value"].lt(0)
    | items["freight_value"].isna()
)

save_outputs("order_items", items)


# ==========================================
# 6. GEOLOCATION
# ==========================================

geo = load_csv(
    "olist_geolocation_dataset.csv",
    dtype={"geolocation_zip_code_prefix": "string"}
)

geo["geolocation_lat"] = pd.to_numeric(
    geo["geolocation_lat"], errors="coerce"
)

geo["geolocation_lng"] = pd.to_numeric(
    geo["geolocation_lng"], errors="coerce"
)

geo["flag_missing_zip"] = geo[
    "geolocation_zip_code_prefix"
].isna()

geo["flag_invalid_zip"] = (
    ~geo["geolocation_zip_code_prefix"]
    .str.fullmatch(r"\d{5}", na=False)
)

geo["flag_invalid_latitude"] = (
    ~geo["geolocation_lat"].between(-90, 90)
)

geo["flag_invalid_longitude"] = (
    ~geo["geolocation_lng"].between(-180, 180)
)

geo["flag_duplicate_record"] = geo.duplicated(keep="first")

save_outputs("geolocation", geo)


# ==========================================
# 7. CATEGORY TRANSLATION
# ==========================================

translation = load_csv(
    "product_category_name_translation.csv"
)

translation["flag_missing_category"] = (
    translation["product_category_name"].isna()
)

translation["flag_missing_english_name"] = (
    translation["product_category_name_english"].isna()
)

translation["flag_duplicate_category"] = (
    translation["product_category_name"].duplicated(keep="first")
)

save_outputs("category_translation", translation)


# ==========================================
# FINAL SUMMARY
# ==========================================

print("\n======================================")
print("ALL REMAINING DATASETS PROCESSED")
print("======================================")

print("\nGenerated processed files:")
for file in sorted(PROCESSED_DIR.glob("*_processed.csv")):
    print(file.name)

print("\nRaw datasets remain unchanged.")
print("No records were deleted or automatically corrected.")
