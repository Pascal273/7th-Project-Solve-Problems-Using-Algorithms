import csv
from math import ceil
from pathlib import Path
from pprint import pprint

BUDGET = 500
count = 0


def create_top_profit_list(csv_dataset):
    """
    Takes a CSV-dataset (share name, price, win in %) and creates a new CSV-file
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
                # exclude non or negative profit shares from the list
                if profit_euro > 0:
                    share_list.append({"name": name, "price(€)": price, "profit(€)": profit_euro})

    # create a new list of only the top profit shares within the MAX_TO_SPEND limit
    best_combination = get_best_combination(share_list, BUDGET)

    total_cost = round(sum(i["price(€)"] for i in best_combination), 2)
    total_profit = round(sum(i["profit(€)"] for i in best_combination), 2)

    # append "footer" with total of cost and profit
    best_combination.append({
        "name": "Total",
        "price(€)": total_cost,
        "profit(€)": total_profit
    })

    # Create and save a new CSV-file from the most profit list
    Path("Optimized CSV Files").mkdir(parents=True, exist_ok=True)
    file_name = "top shares of " + csv_dataset.split(".")[0]
    field_names = [key for key, value in best_combination[0].items()]
    with open(f"Optimized CSV Files/{file_name}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(best_combination)


def get_best_combination(share_list, budget):
    """
    Takes a list of share objects (dictionary format) and a max-budget and returns
    the combination with the highest profit that doesn't exceed the budget.

    Args:
        share_list: list     - list of dictionaries in format of:
                               {"name": x, "price(€)": x,xx, "profit(€)": x,xx}
        budget: int - the max budget that isn't allowed to be exceeded.
    """
    # n = number of shares
    n = len(share_list)

    # create empty table
    table = [[[] for b in range(budget + 1)] for i in range(n + 1)]

    # populate table in bottom up manner
    for i in range(n + 1):
        for b in range(budget + 1):
            if i == 0 or b == 0:
                table[i][b] = []
            elif ceil(share_list[i - 1]["price(€)"]) <= b:
                case1 = table[i - 1][b - ceil(share_list[i - 1]["price(€)"])] + [share_list[i - 1]]
                case2 = table[i - 1][b]
                value1 = sum(i["profit(€)"] for i in case1)
                value2 = sum(i["profit(€)"] for i in case2)
                if value1 > value2:
                    table[i][b] = case1
                else:
                    table[i][b] = case2
            else:
                table[i][b] = table[i - 1][b]

    # get and return result
    res = list(table[n][budget])
    return res
