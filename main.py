import bruteforce
import optimized
from timeit import default_timer as timer
import tracemalloc as memory

BUDGET = 500

DATASET_TEST = "dataset_test.csv"

DATASET_1 = "dataset1_Python+P7.csv"
DATASET_2 = "dataset2_Python+P7.csv"


def time_optimized(data):
    """Displays the time the optimized algorithm needed to execute"""
    start = timer()
    optimized.create_top_profit_list(data)
    end = timer()
    print(f"Optimized needed {end - start} seconds.")


def time_bruteforce(data):
    """Displays the time the bruteforce algorithm needed to execute"""
    start = timer()
    bruteforce.create_top_profit_list(data)
    end = timer()
    print(f"Bruteforce needed {end - start} seconds.")


def memory_bruteforce(data):
    """Displays the peak memory used by the bruteforce algorithm"""
    memory.start()
    bruteforce.create_top_profit_list(data)
    used_memory = round(memory.get_traced_memory()[1] / 1000000, 2)
    print(f"Bruteforce used up to {used_memory} MB of memory.")
    memory.stop()


def memory_optimized(data):
    """Displays the peak memory used by the optimized algorithm"""
    memory.start()
    optimized.create_top_profit_list(data)
    used_memory = round(memory.get_traced_memory()[1] / 1000000, 2)
    print(f"Optimized used up to {used_memory} MB of memory.")
    memory.stop()


if __name__ == '__main__':
    # bruteforce.create_top_profit_list(DATASET_TEST, BUDGET)
    optimized.create_top_profit_list(DATASET_1, BUDGET)
    optimized.create_top_profit_list(DATASET_2, BUDGET)
