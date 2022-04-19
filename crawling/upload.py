import time
from pathlib import Path

import pandas as pd

from settings import engine


BASE_DIR = str(Path(__file__).resolve().parent)


def main():
    df_cafe_list = pd.read_csv(
        f"{BASE_DIR}/csv/cafes.csv", encoding="utf-8", header=None
    )
    df_rep_num = pd.read_csv(
        f"{BASE_DIR}/csv/phone_numbers.csv", encoding="utf-8", header=None
    )

    df_cafes = pd.merge(left=df_cafe_list, right=df_rep_num, how="left", on=0)
    df_cafes.columns = ["place_id", "name", "address", "lat", "lon", "rep_number"]
    df_cafes.drop_duplicates(["name"], inplace=True)
    df_cafes.drop(columns=['place_id'], inplace=True)

    df_cafes.to_sql(
        index=False,
        name="cafes",
        con=engine,
        if_exists="append",
        method="multi",
    )


if __name__ == "__main__":
    start = time.time()
    main()
    delta = time.time() - start
    print(f"소요시간: {delta:.03}")
