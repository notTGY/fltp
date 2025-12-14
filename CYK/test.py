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

        if naive_result == fast_result:
            print(f"Test {i}: PASS - Results match")
        else:
            print(f"Test {i}: FAIL - Results differ")
            print("Naive:", naive_result)
            print("Fast:", fast_result)


N = 100


def test_performance():
    print("\nTesting performance...")
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


if __name__ == "__main__":
    test_correctness()
    test_performance()
