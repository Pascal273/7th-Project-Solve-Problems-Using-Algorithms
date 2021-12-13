import csv
from itertools import combinations
from pathlib import Path

MAX_TO_SPEND = 500


def create_top_profit_list(csv_dataset):
    """
    Takes a CSV-dataset (share name, price, profit in %) and creates a new CSV-file
    with the top profit shares only within a total price of >MAX_TO_SPEND< €.
    """

    # read the dataset-file and get the required values
    with open(csv_dataset, newline="") as dataset:
        data = csv.reader(dataset, delimiter=",")

        # get share-name, price and profit in % of each share
        share_list = []
        for row in data:
            if row[0] != "name":
                name = row[0]
                price = float(row[1])
                profit_percent = float(row[2])

                profit_euro = round((price / 100 * profit_percent), 2)
                if price > 0 and profit_euro > 0:
                    share_list.append({"name": name, "price(€)": price, "profit(€)": profit_euro})


        # Create and save a new CSV-file from the most profit list
        Path("Bruteforce CSV Files").mkdir(parents=True, exist_ok=True)
        file_name = "top shares of " + csv_dataset.split(".")[0]
        field_names = [key for key, value in best_combination[0].items()]
        with open(f"Bruteforce CSV Files/{file_name}.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(best_combination)
