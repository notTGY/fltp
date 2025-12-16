import time
import copy
import sys
import os
from contextlib import redirect_stdout
from naive import CYK_graph as naive_CYK
from fast import CYK_graph as fast_CYK

graph1 = [
    ["0", "a", "0", "0", "0"],
    ["0", "0", "d", "0", "0"],
    ["0", "0", "0", "d", "0"],
    ["0", "0", "0", "0", "c"],
    ["0", "0", "0", "0", "0"],
]

graph2 = [
    ["0", "a", "0", "0", "0"],
    ["0", "0", "d", "0", "0"],
    ["0", "0", "0", "d", "0"],
    ["0", "0", "0", "c", "c"],
    ["0", "0", "0", "0", "0"],
]


def test_correctness():
    print("Testing correctness...")
    for i, graph in enumerate([graph1, graph2], 1):
        naive_result = copy.deepcopy(graph)
        fast_result = copy.deepcopy(graph)

        naive_CYK(naive_result, log=False)
        fast_CYK(fast_result, log=False)

        # Sort inner lists for consistent comparison
        for row in naive_result:
            for cell in row:
                cell.sort()
        for row in fast_result:
            for cell in row:
                cell.sort()

        if naive_result == fast_result:
            print(f"Test {i}: PASS - Results match")
        else:
            print(f"Test {i}: FAIL - Results differ")
            print("Naive:", naive_result)
            print("Fast:", fast_result)


N = 1000


def test_performance():
    print("\nTesting performance on small graph (n=5)...")
    graph = graph1
    start = time.time()
    with redirect_stdout(open(os.devnull, "w")):
        for _ in range(N):
            test_graph = copy.deepcopy(graph)
            naive_CYK(test_graph, log=False)
    naive_time = time.time() - start

    start = time.time()
    for _ in range(N):
        test_graph = copy.deepcopy(graph)
        fast_CYK(test_graph, log=False)
    fast_time = time.time() - start

    print(
        f"Naive: {naive_time:.4f}s, Fast: {fast_time:.4f}s, Speedup: {naive_time / fast_time:.2f}x"
    )

    # Larger test case
    print("\nTesting performance on larger graph (n=10)...")
    n_large = 10
    graph_large = [["0" for _ in range(n_large)] for _ in range(n_large)]
    # Add some terminals
    for i in range(n_large):
        if i % 2 == 0:
            graph_large[i][i] = "a"
        if i + 1 < n_large:
            graph_large[i][i + 1] = "d"
        if i + 2 < n_large:
            graph_large[i + 1][i + 2] = "c"

    N_large = max(1, N // 100)  # reduce N for larger n to keep time reasonable

    start = time.time()
    with redirect_stdout(open(os.devnull, "w")):
        for _ in range(N_large):
            test_graph = copy.deepcopy(graph_large)
            naive_CYK(test_graph, log=False)
    naive_time_large = time.time() - start

    start = time.time()
    for _ in range(N_large):
        test_graph = copy.deepcopy(graph_large)
        fast_CYK(test_graph, log=False)
    fast_time_large = time.time() - start

    print(
        f"Naive: {naive_time_large:.4f}s, Fast: {fast_time_large:.4f}s, Speedup: {naive_time_large / fast_time_large:.2f}x"
    )


if __name__ == "__main__":
    test_correctness()
    test_performance()
