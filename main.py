import bruteforce
import optimized

BUDGET = 500

DATASET_TEST = "dataset_test.csv"

DATASET_1 = "dataset1_Python+P7.csv"
DATASET_2 = "dataset2_Python+P7.csv"

if __name__ == '__main__':
    bruteforce.create_top_profit_list(DATASET_TEST, BUDGET)
    optimized.create_top_profit_list(DATASET_TEST, BUDGET)
    optimized.create_top_profit_list(DATASET_1, BUDGET)
    optimized.create_top_profit_list(DATASET_2, BUDGET)
