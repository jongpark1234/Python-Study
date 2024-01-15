import ray
import time

ray.init()

@ray.remote
def partial_sum(start: int, end: int) -> int:
    return sum(range(start, end + 1))

def parallel_sum(start: int, end: int) -> int:
    total_sum = 0
    process_num = 8
    chunk_size, remainder = divmod(end - start + 1, process_num)

    futures = []
    for i in range(process_num):
        end = start + chunk_size - 1 + remainder * (i == 0)
        futures.append(partial_sum.remote(start, end))
        start = end + 1

    partial_sums = ray.get(futures)
    total_sum = sum(partial_sums)

    return total_sum

if __name__ == "__main__":
    start, end = 1, 100_000_000
    start_time = time.time()
    print(parallel_sum(start, end))
    end_time = time.time()
    print(end_time - start_time)

    ray.shutdown()