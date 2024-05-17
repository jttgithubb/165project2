# Module for benchmarking different bin-packing algorithms on different input sizes n and waste W(A)
# 1. Enter the algorithm name and number of items
# 2. Run benchmark and calculate the waste (10 datapoints per size n)
# 3. Record in a separate csv file for each algorithm

from next_fit import next_fit
from first_fit import first_fit, first_fit_decreasing
from best_fit import best_fit, best_fit_decreasing
import argparse
import random
from pathlib import Path

DATA_DIRECTORY = Path('data')

PACKING_ALGORITHMS = {
    'next_fit': next_fit,
    'first_fit': first_fit,
    'first_fit_decreasing': first_fit_decreasing,
    'best_fit': best_fit,
    'best_fit_decreasing': best_fit_decreasing
}

parser = argparse.ArgumentParser(
    prog= 'Benchmark',
    description= 'Benchmarking different bin-packing algorithms on different input sizes n and waste W(A)',
    epilog= 'Happy bin-packing!'
)
parser.add_argument('algorithm', choices=PACKING_ALGORITHMS.keys(), help='Bin-packing algorithm')
parser.add_argument('size', type=int, help='Size of input list')

def get_waste(items: list[float], free_space: list[float]):
    return float(len(free_space)) - sum(items)

def generate_random_list(size: int):
    a = 0.0 + 1e-10
    b = 0.4 - 1e-10
    float_list = []
    for i in range(size):
        num_f = random.uniform(a, b)
        float_list.append(num_f)
    return float_list

def get_data_path(algorithm_name: str):
    directory = DATA_DIRECTORY / algorithm_name
    directory.mkdir(parents=True, exist_ok=True)
    return (directory / algorithm_name).with_suffix('.csv')

def run_benchmark(algorithm, size: int):
    items = generate_random_list(size)
    n = len(items)
    assignment = [0 for i in range(n)]
    free_space = []
    algorithm(items, assignment, free_space)
    waste = get_waste(items, free_space)
    return size,waste

if __name__ == "__main__":
    args = parser.parse_args()
    data_path = get_data_path(args.algorithm)
    with open(data_path, 'a') as f:
        for i in range(10):
            size, waste = run_benchmark(PACKING_ALGORITHMS[args.algorithm], args.size)
            f.write(f"{size} {waste}\n")
