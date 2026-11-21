
import os
import logging
import pandas as pd
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert


from backend.app.database import engine
from backend.app.models.customer import Customer
from backend.app.models.seller import Seller
from backend.app.models.product import Product
from backend.app.models.category_translation import CategoryTranslation
from backend.app.models.order import Order
from backend.app.models.order_item import OrderItem
from backend.app.models.payment import Payment
from backend.app.models.review import Review
from backend.app.models.geolocation import Geolocation


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "etl.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("ETL")


DATASETS = [
    {
        "file": "customers_processed.csv",
        "model": Customer,
        "columns": [
            "customer_id",
            "customer_unique_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state"
        ],
        "dtype": {"customer_zip_code_prefix": "string"}
    },
    {
        "file": "sellers_processed.csv",
        "model": Seller,
        "columns": [
            "seller_id",
            "seller_zip_code_prefix",
            "seller_city",
            "seller_state"
        ],
        "dtype": {"seller_zip_code_prefix": "string"}
    },
    {
        "file": "products_processed.csv",
        "model": Product,
        "columns": [
            "product_id",
            "product_category_name",
            "product_name_length",
            "product_description_length",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ],
        "rename": {
            "product_name_lenght": "product_name_length",
            "product_description_lenght": "product_description_length"
        }
    },
    {
        "file": "category_translation_processed.csv",
        "model": CategoryTranslation,
        "columns": [
            "product_category_name",
            "product_category_name_english"
        ]
    },
    {
        "file": "orders_processed.csv",
        "model": Order,
        "columns": [
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ],
        "dates": [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    },
    {
        "file": "order_items_processed.csv",
        "model": OrderItem,
        "columns": [
            "order_id",
            "order_item_id",
            "product_id",
            "seller_id",
            "shipping_limit_date",
            "price",
            "freight_value"
        ],
        "dates": ["shipping_limit_date"]
    },
    {
        "file": "payments_processed.csv",
        "model": Payment,
        "columns": [
            "order_id",
            "payment_sequential",
            "payment_type",
            "payment_installments",
            "payment_value"
        ]
    },
    {
    "file": "reviews_processed.csv",
    "model": Review,
    "columns": [
        "review_id",
        "order_id",
        "review_score",
        "review_comment_title",
        "review_comment_message",
        "review_creation_date",
        "review_answer_timestamp"
    ],
    "dates": [
        "review_creation_date",
        "review_answer_timestamp"
    ]
},
    {
    "file": "geolocation_processed.csv",
    "model": Geolocation,
    "columns": [
        "geolocation_zip_code_prefix",
        "geolocation_lat",
        "geolocation_lng",
        "geolocation_city",
        "geolocation_state"
    ],
    "dtype": {
        "geolocation_zip_code_prefix": "string"
    },
    "batch_size": 5000,
    "truncate_before_load": True

}
]


def load_dataset(config):
    file_path = os.path.join(DATA_DIR, config["file"])

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    batch_size = config.get("batch_size", 5000)
    total_processed = 0

    print(f"\nLoading: {config['file']}")
    logger.info("Starting dataset: %s", config["file"])

    try:
        with engine.begin() as connection:

            if config.get("truncate_before_load"):
                connection.execute(
                    text("TRUNCATE TABLE geolocation RESTART IDENTITY")
                )

            for chunk in pd.read_csv(
                file_path,
                chunksize=batch_size,
                dtype=config.get("dtype")
            ):
                if config.get("rename"):
                    chunk = chunk.rename(columns=config["rename"])

                for column in config.get("dates", []):
                    chunk[column] = pd.to_datetime(
                        chunk[column],
                        errors="coerce"
                    )

                chunk = chunk[config["columns"]]

                chunk = chunk.astype(object).where(
                    pd.notna(chunk),
                    None
                )

                records = chunk.to_dict(orient="records")

                if records:
                    statement = (
                        insert(config["model"].__table__)
                        .values(records)
                        .on_conflict_do_nothing()
                    )

                    connection.execute(statement)

                total_processed += len(records)

                print(
                    f"\rProcessed: {total_processed:,} rows",
                    end=""
                )

        print(f"\nCompleted: {config['file']}")
        print(f"Rows processed: {total_processed:,}")

        logger.info(
            "Completed dataset: %s | Rows processed: %s",
            config["file"],
            total_processed
        )

        return total_processed

    except Exception:
        logger.exception("Failed dataset: %s", config["file"])
        raise
def main():
    print("=" * 55)
    print("E-COMMERCE DATA ETL")
    print("CSV TO POSTGRESQL")
    print("=" * 55)

    logger.info("ETL process started")

    dataset_summary = {}
    grand_total = 0

    try:
        for config in DATASETS:
            total = load_dataset(config)

            dataset_summary[config["file"]] = total
            grand_total += total

        print("\n" + "=" * 55)
        print("ETL EXECUTION SUMMARY")
        print("=" * 55)

        for filename, count in dataset_summary.items():
            print(f"{filename}: {count:,}")

        print("-" * 55)
        print(f"TOTAL ROWS PROCESSED: {grand_total:,}")
        print("ALL DATASETS PROCESSED SUCCESSFULLY")
        print("=" * 55)

        logger.info(
            "ETL completed successfully | Datasets: %s | Rows processed: %s",
            len(dataset_summary),
            grand_total
        )

    except Exception:
        logger.exception("ETL process failed")
        raise

if __name__ == "__main__":
    main()
