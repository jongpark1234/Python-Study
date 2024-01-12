import time
import concurrent.futures
import multiprocessing
from typing import List, Tuple

def get_ranges_array(start: int, end: int, divisor: int) -> List[Tuple[int]]:
    step = (end - start + 1) // divisor
    return [(i, i + step - 1) for i in range(start, end + 1, step)]


def calculate_sum(ranges: Tuple[int]) -> int:
    total_sum = 0
    start, end = ranges
    for i in range(start, end + 1):
        total_sum += i
    return total_sum
        

def do_threading(ranges: Tuple[int]) -> None:
    start, end = ranges
    num_threads = 2
    
    thread_ranges = get_ranges_array(start, end, num_threads)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        return list(executor.map(calculate_sum, thread_ranges))


def do_processing() -> None:
    start, end = 1, 100000
    num_processes = 4

    process_ranges = get_ranges_array(start, end, num_processes)
    
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(do_threading, process_ranges)
        print(sum(sum(result) for result in results))
    

if __name__ == "__main__":
    start_time = time.time()
    do_processing()
    end_time = time.time()
    parallel = end_time - start_time
    
    start_time = time.time()
    print(sum(i for i in range(1, 100001)))
    end_time = time.time()
    serial = end_time - start_time
    print(parallel, serial)
