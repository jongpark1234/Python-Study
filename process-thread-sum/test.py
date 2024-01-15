import ray
import time

ray.init()

@ray.remote
def partial_sum(start: int, end: int) -> int:
    return sum(range(start, end + 1))

def parallel_sum(start: int, end: int) -> int:
    total_sum = 0
    process_num = 8
    chunk_size = (end - start + 1) // process_num
    remainder = (end - start + 1) % process_num

    futures = []
    current_start = start
    for _ in range(process_num):
        current_end = current_start + chunk_size - 1
        if remainder > 0:
            current_end += 1
            remainder -= 1

        futures.append(partial_sum.remote(current_start, current_end))
        current_start = current_end + 1

    partial_sums = ray.get(futures)
    total_sum = sum(partial_sums)

    return total_sum

if __name__ == "__main__":
    start, end = 1, 100_000_000
    start_time = time.time()
    print(parallel_sum(start, end))
    end_time = time.time()
    print(end_time - start_time)

    # Ray를 종료합니다.
    ray.shutdown()