import pandas as pd
from pathlib import Path

DATA_DIR = Path(r"D:\AWS-Ecommerce-Data-Intelligence\data\raw")

for file in DATA_DIR.glob("*.csv"):
    print("\n" + "=" * 60)
    print("FILE:", file.name)

    try:
        df = pd.read_csv(file)

        print("Rows:", df.shape[0])
        print("Columns:", df.shape[1])
        print("File Size (MB):", round(file.stat().st_size / (1024 * 1024), 2))

        print("\nColumn Names:")
        print(list(df.columns))

        print("\nMissing Values:")
        print(df.isnull().sum())

        print("\nDuplicate Rows:", df.duplicated().sum())

        print("\nData Types:")
        print(df.dtypes)

    except Exception as e:
        print("Error:", e)
