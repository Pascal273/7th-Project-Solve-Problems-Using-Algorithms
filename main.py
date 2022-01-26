import bruteforce
import optimized
import space_optimzed

BUDGET = "500"

if __name__ == '__main__':
    dataset = input("Please enter (or copy and paste) the path of the csv-dataset:\n")
    budget = ""
    while not budget.isdigit():
        budget = input("What's the budget/max cost? (Press enter for default 500)") or BUDGET
    budget = int(budget)

    algorithm = input("Please enter:\n"
                      "[O] to use the optimized algorithm\n"
                      "[S] to use the space-optimized algorithm\n"
                      "[B] to use the bruteforce method\n"
                      "WARNING! Bruteforce can't be used on files with much more than 20 shares\n"
                      ).lower()

    if algorithm == "b":
        bruteforce.create_top_profit_list(dataset, budget)

    elif algorithm == "s":
        space_optimzed.create_top_profit_list(dataset, budget)

    else:
        optimized.create_top_profit_list(dataset, budget)

    print("Optimal result files successfully created!")
