import csv
from pathlib import Path


def create_top_profit_list(csv_dataset, budget):
    """
    Takes a CSV-dataset (share name, price, profit in %) and creates a new CSV-file
    with the top profit shares only within a total price of >MAX_TO_SPEND< €.

    Args:
        csv_dataset: str - path to csv-file
        budget: int - budget (maximum total costs)
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

    if len(share_list) > 20:
        raise OverflowError("The share list has to many positions (max. 20 allowed!)")

    # get best result
    best_combination = get_best_combination(share_list, budget)

    # append "footer" with total of cost and profit
    total_cost = round(sum(i["price(€)"] for i in best_combination), 2)
    total_profit = round(sum(i["profit(€)"] for i in best_combination), 2)
    best_combination.append({
        "name": "Total",
        "price(€)": total_cost,
        "profit(€)": total_profit
    })

    # Create and save a new CSV-file from the most profit list
    Path("Bruteforce CSV Files").mkdir(parents=True, exist_ok=True)
    file_name = "top shares of " + csv_dataset.split("\\")[-1].split(".")[0]
    field_names = [key for key, value in best_combination[0].items()]
    with open(f"Bruteforce CSV Files/{file_name}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(best_combination)


def get_best_combination(share_list, budget, n=None, combination=None):
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

    # at first call n = number of shares in list
    if n is None:
        n = len(share_list)

    # at first call create empty list for combinations
    if combination is None:
        combination = []
    current_total = sum(i["price(€)"] for i in combination)

    # get current share
    share = share_list[n - 1]

    # base Case
    if n == 0:
        return combination

    # if current total price + next share price exceeds the budget,
    # the current share can't be included
    if current_total + share["price(€)"] > budget:
        return get_best_combination(share_list, budget, n - 1, combination)

    # case 1: share included in the optimal solution
    # case 2: not included
    else:
        case_1 = get_best_combination(share_list, budget, n - 1, combination + [share])
        case_2 = get_best_combination(share_list, budget, n - 1, combination)
        value1 = sum(i["profit(€)"] for i in case_1)
        value2 = sum(i["profit(€)"] for i in case_2)

        if value1 > value2:
            return case_1
        else:
            return case_2
