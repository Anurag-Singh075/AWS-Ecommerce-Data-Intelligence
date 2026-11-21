# Olist Brazilian E-Commerce Dataset --- Data Quality Report

**Project:** AWS E-Commerce Data Intelligence Platform\
**Dataset:** Brazilian E-Commerce Public Dataset by Olist\
**Validation stage:** Initial raw-data profiling and quality checks\
**Status:** Analysis completed; raw files preserved without modification

------------------------------------------------------------------------

## 1. Dataset overview

The raw dataset contains 9 CSV files and **1,550,922 total rows** across
all files.

  File                                                 Rows   Columns
  ----------------------------------------- --------------- ---------
  `olist_customers_dataset.csv`                      99,441         5
  `olist_geolocation_dataset.csv`                 1,000,163         5
  `olist_orders_dataset.csv`                         99,441         8
  `olist_order_items_dataset.csv`                   112,650         7
  `olist_order_payments_dataset.csv`                103,886         5
  `olist_order_reviews_dataset.csv`                  99,224         7
  `olist_products_dataset.csv`                       32,951         9
  `olist_sellers_dataset.csv`                         3,095         4
  `product_category_name_translation.csv`                71         2
  **Total**                                   **1,550,922**       ---

Approximate raw dataset size: **126.18 MB**.

## 2. Table-level missing values and duplicate observations

### Customers

-   Rows: 99,441
-   Missing values: none
-   Duplicate full rows: 0

### Geolocation

-   Rows: 1,000,163
-   Missing values: none
-   Duplicate full rows: 261,831

The repeated geolocation rows have been identified during profiling.
They have not been removed from the raw file.

### Orders

-   Rows: 99,441
-   Missing `order_approved_at`: 160
-   Missing `order_delivered_carrier_date`: 1,783
-   Missing `order_delivered_customer_date`: 2,965
-   No duplicate full rows detected.

### Order items

-   Rows: 112,650
-   Missing values: none
-   Duplicate full rows: 0

### Payments

-   Rows: 103,886
-   Missing values: none
-   Duplicate full rows: 0

### Reviews

-   Rows: 99,224
-   Missing `review_comment_title`: 87,656
-   Missing `review_comment_message`: 58,247
-   No duplicate full rows detected.

A review ID alone is not a unique key in this dataset. Composite
validation using (`review_id`, `order_id`) found no duplicate
combinations.

### Products

-   Rows: 32,951
-   Missing `product_category_name`: 610
-   Missing `product_name_lenght`: 610
-   Missing `product_description_lenght`: 610
-   Missing `product_photos_qty`: 610
-   Missing `product_weight_g`: 2
-   Missing `product_length_cm`: 2
-   Missing `product_height_cm`: 2
-   Missing `product_width_cm`: 2
-   No duplicate full rows detected.

### Sellers

-   Rows: 3,095
-   Missing values: none
-   Duplicate full rows: 0

### Product category translation

-   Rows: 71
-   Missing values: none
-   Duplicate full rows: 0

## 3. Key and relationship validation

Primary-key checks:

  Table       Key               Duplicate keys
  ----------- --------------- ----------------
  Customers   `customer_id`                  0
  Orders      `order_id`                     0
  Products    `product_id`                   0
  Sellers     `seller_id`                    0

For reviews, the composite key (`review_id`, `order_id`) had **0
duplicate combinations**. `review_id` by itself repeats 814 times, so it
should not be treated as a unique key without further business context.

Foreign-key checks:

  Relationship                           Orphan records
  ------------------------------------ ----------------
  Orders → Customers (`customer_id`)                  0
  Items → Orders (`order_id`)                         0
  Items → Products (`product_id`)                     0
  Items → Sellers (`seller_id`)                       0
  Payments → Orders (`order_id`)                      0
  Reviews → Orders (`order_id`)                       0

All tested foreign-key relationships passed the orphan-record checks.

## 4. Numeric data quality checks

### Order items

-   `price` less than or equal to zero: 0
-   Negative `freight_value`: 0
-   `order_item_id` less than or equal to zero: 0

### Payments

-   `payment_value` less than or equal to zero: **9**
-   Negative `payment_installments`: 0

Investigation of the 9 zero-value payment rows: - They use payment types
`voucher` and `not_defined`. - They belong to 7 affected orders. - 4
affected orders also contain positive-value payment rows. - 3 affected
orders contain only zero-value payment rows. - One order
(`fa65dad1b0e818e3ccc5cb0e39231352`) has 29 payment rows, including two
zero-value rows, and a total payment value of 457.99.

These observations are flagged for business-rule review. Zero-value rows
are not automatically classified as invalid or deleted.

### Reviews

-   `review_score` outside the expected 1--5 range: 0

### Products

-   `product_weight_g` less than or equal to zero: **4**
-   Non-positive product length, height, or width: 0

The four zero-weight products are: -
`81781c0fed9fe1ad6e8c81fca1e1cb08` -
`8038040ee2a71048d4bdbbdc985b69ab` -
`36ba42dd187055e1fbe943b2d11430ca` - `e673e90efa65a5409ff4196c038bb5af`

All four belong to category `cama_mesa_banho` and have dimensions 30 ×
25 × 30 cm. Their weights require review; no weight has been imputed.

## 5. Date and timestamp quality

Missing timestamp counts in the orders table:

  Timestamp                           Missing rows
  --------------------------------- --------------
  `order_purchase_timestamp`                     0
  `order_approved_at`                          160
  `order_delivered_carrier_date`             1,783
  `order_delivered_customer_date`            2,965
  `order_estimated_delivery_date`                0

Date sequence checks:

  Check                                         Violating rows
  ------------------------------------------- ----------------
  Approval before purchase                                   0
  Carrier dispatch before purchase                         166
  Customer delivery before purchase                          0
  Customer delivery before carrier dispatch                 23
  Estimated delivery before purchase                         0

The 166 carrier-before-purchase records and 23 delivery-before-carrier
records are timestamp-sequence anomalies. Example records were
inspected. The original timestamps have not been changed.

## 6. Order status validation

Order status distribution:

  Order status         Orders
  -------------- ------------
  delivered            96,478
  shipped               1,107
  canceled                625
  unavailable             609
  invoiced                314
  processing              301
  created                   5
  approved                  2
  **Total**        **99,441**

Status and timestamp mismatches found:

  Check                                                    Records
  ------------------------------------------------------ ---------
  Delivered orders missing customer-delivery timestamp           8
  Delivered orders missing carrier timestamp                     2
  Canceled orders with customer-delivery timestamp               6

The 8 delivered orders missing customer-delivery timestamps, 2 delivered
orders missing carrier timestamps, and 6 canceled orders with delivery
timestamps were inspected. One order appears in both delivered-order
checks, so these counts should not be added as unique orders.

These records are flagged for later investigation rather than being
automatically relabeled or removed.

## 7. Recommended handling in the processed-data layer

The following are recommendations for a later, explicitly defined
transformation stage---not changes already applied:

1.  Preserve all raw CSV files as the source of truth.
2.  Convert timestamp columns to proper datetime types in processed
    outputs.
3.  Create explicit quality flags for invalid timestamp sequences and
    status/timestamp mismatches.
4.  Keep missing timestamps as missing unless a documented business rule
    supports a specific treatment.
5.  Review zero-value payments and zero product weights before deciding
    whether to exclude, retain, or specially classify them.
6.  Decide how to handle duplicate geolocation rows based on the
    intended analytical grain and downstream use.
7.  Retain missing review comments as null values; do not treat an
    absent optional comment as a failed review.
8.  Document every transformation and its row counts so results can be
    traced back to the raw dataset.

## 8. Validation conclusion

-   Dataset inspection completed for all 9 CSV files.
-   Primary-key checks passed for the tested entity keys.
-   All 6 tested foreign-key relationships had zero orphan records.
-   Numeric, date-sequence, and order-status anomalies were identified
    and documented.
-   Raw data has **not** been cleaned, overwritten, or modified.

**Overall result:** Initial raw-data profiling and validation are
complete. The identified anomalies must be handled through documented
rules in a later processed-data stage.
