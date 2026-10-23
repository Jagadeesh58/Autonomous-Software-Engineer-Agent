"""
data.py - Sample Pandas data analysis script.
"""

import os
import pandas as pd

CSV_PATH = os.path.join(os.path.dirname(__file__), "data.csv")


def analyze_data():
    if not os.path.exists(CSV_PATH):
        print(f"File not found: {CSV_PATH}")
        return

    data = pd.read_csv(CSV_PATH)
    avg_price = data["price"].mean()
    max_item = data.loc[data["price"].idxmax()]
    min_item = data.loc[data["price"].idxmin()]

    print("--- Data Summary ---")
    print(f"Total Items:   {len(data)}")
    print(f"Average Price: ${avg_price:.2f}")
    print(f"Highest Price: {max_item['name']} (${max_item['price']})")
    print(f"Lowest Price:  {min_item['name']} (${min_item['price']})")


if __name__ == "__main__":
    analyze_data()
