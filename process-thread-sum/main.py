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
        

def do_threading(ranges: Tuple[int]) -> List[List[int]]:
    num_threads = 2
    start, end = ranges
    thread_ranges = get_ranges_array(start, end, num_threads)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        return list(executor.map(calculate_sum, thread_ranges))


def do_processing(start: int, end: int) -> None:
    num_processes = 4
    process_ranges = get_ranges_array(start, end, num_processes)
    
    with multiprocessing.Pool(processes=num_processes) as pool:
        return sum(map(sum, pool.map(do_threading, process_ranges)))
    

if __name__ == "__main__":
    start, end = 1, 100_000
    start_time = time.time()
    print(do_processing(start, end))
    end_time = time.time()
    parallel = end_time - start_time
    
    start_time = time.time()
    print(sum(i for i in range(start, end + 1)))
    end_time = time.time()
    serial = end_time - start_time
    
    print(parallel, serial)
