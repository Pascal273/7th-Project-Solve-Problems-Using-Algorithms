import csv
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

    # sort list (lowest -> highest profit) to start with the top-profit shares
    sorted_list = sorted(share_list, key=lambda x: x["profit(€)"])

    # create a new list of only the top profit shares within the MAX_TO_SPEND limit
    best_combination = get_best_combination(sorted_list, BUDGET)

    pprint(best_combination)
    total_cost = round(sum(i["price(€)"] for i in best_combination), 2)
    total_profit = round(sum(i["profit(€)"] for i in best_combination), 2)

    print("total cost: ", total_cost)
    print("total profit", total_profit)
    print("Recursion ran", count, " times")

    # Create and save a new CSV-file from the most profit list
    # Path("Optimized CSV Files").mkdir(parents=True, exist_ok=True)
    # file_name = "top shares of " + csv_dataset.split(".")[0]
    # field_names = [key for key, value in best_combination[0].items()]
    # with open(f"Optimized CSV Files/{file_name}.csv", "w", newline="", encoding="utf-8") as file:
    #     writer = csv.DictWriter(file, fieldnames=field_names)
    #     writer.writeheader()
    #     writer.writerows(best_combination)


def get_best_combination(share_list, budget, n=None, combination=None, memo=None):
    """
    Takes a list of share objects (dictionary format) and a max-budget and returns
    the combination with the highest profit that doesn't exceed the budget.

    Args:
        share_list: list     - list of dictionaries in format of:
                               {"name": x, "price(€)": x,xx, "profit(€)": x,xx}
        budget: int or float - the max budget that isn't allowed to be exceeded.
        n : int              - the number of items in share_list
        combination: list    - list of possible combinations that will be created
                               and compared and eliminated during the process
    """

    global count
    count += 1

    # at first call n = number of shares in list
    if n is None:
        n = len(share_list)

    # at first call create empty list for combinations
    if combination is None:
        combination = []
    current_total = sum(i["price(€)"] for i in combination)

    if memo is None:
        memo = {}

    m = f"{n}, {int(current_total)}"

    if m in memo:
        return memo[m]

    # get current share
    share = share_list[n - 1]

    # base Case
    if n == 0:
        return combination

    # if current total price exceeds the budget, the current share can't be included
    if current_total + share["price(€)"] > budget:
        memo[m] = get_best_combination(share_list, budget, n - 1, combination, memo)
        return memo[m]

    # case 1: share included in the optimal solution
    # case 2: not included
    else:
        case_1 = get_best_combination(share_list, budget, n - 1, combination + [share], memo)
        case_2 = get_best_combination(share_list, budget, n - 1, combination, memo)
        value1 = sum(i["profit(€)"] for i in case_1)
        value2 = sum(i["profit(€)"] for i in case_2)

        if value1 > value2:
            memo[m] = case_1
            return memo[m]
        else:
            memo[m] = case_2
            return memo[m]

