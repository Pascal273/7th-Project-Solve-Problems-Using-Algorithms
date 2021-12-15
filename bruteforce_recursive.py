import csv
from pprint import pprint
from itertools import combinations
from pathlib import Path

BUDGET = 500


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

        n = len(share_list)
        combi = knapsack(share_list, BUDGET, n)
        pprint(combi)
        print("Price Total: ", round(sum(i["price(€)"] for i in combi), 2))
        print("Profit Total: ", round(sum(i["profit(€)"] for i in combi), 2))

    # Create and save a new CSV-file from the most profit list
    # Path("Bruteforce Recursive CSV Files").mkdir(parents=True, exist_ok=True)
    # file_name = "top shares of " + csv_dataset.split(".")[0]
    # field_names = [key for key, value in best_combination[0].items()]
    # with open(f"Bruteforce Recursive CSV Files/{file_name}.csv", "w", newline="", encoding="utf-8") as file:
    #     writer = csv.DictWriter(file, fieldnames=field_names)
    #     writer.writeheader()
    #     writer.writerows(best_combination)


def knapsack(share_list, budget, n, combination=None):
    if combination is None:
        combination = []
    current_total = sum(i["price(€)"] for i in combination)

    share = share_list[n - 1]
    price = share["price(€)"]

    # base Case
    if n == 0:
        # print("end of list or too expensive!")
        return combination

    if current_total + price > budget:
        return knapsack(share_list, budget, n-1, combination)

    # case 1: share included in the optimal solution
    # case 2: not included
    else:
        case_1 = knapsack(share_list, budget, n-1, combination + [share])
        case_2 = knapsack(share_list, budget, n-1, combination)
        value1 = sum(i["profit(€)"] for i in case_1)
        value2 = sum(i["profit(€)"] for i in case_2)

        if value1 > value2:
            # print("case_1!")
            return case_1
        else:
            # print("case_2!")
            return case_2
