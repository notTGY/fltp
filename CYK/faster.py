import copy

G = {
    "A": [["a"]],
    "B": [["d"]],
    "C": [["c"]],
    "D": [["A", "B"]],
    "E": [["B", "C"]],
    "S": [["D", "E"]],
}


def search_lhs_non_terminal_rule(first, second, log):
    rule = [first, second]
    res = []
    for k, v in G.items():
        for item in v:
            if rule == item:
                res.append(k)
                if log: print("==rule found:", first, second, "<-", k)
    return res


lhs_term_cache = {}
for k, v in G.items():
    for rhs_item in v:
        if len(rhs_item) == 1:
            term = rhs_item[0]
            s = lhs_term_cache.get(term, set())
            s.add(k)
            lhs_term_cache[term] = s


def search_lhs_terminal_rule(term=None):
    return list(lhs_term_cache.get(term, {}))


def logM(M, prefix_msg=None, postfix_msg=None):
    if prefix_msg:
        print(prefix_msg)

    # Find the maximum width needed for any element in the matrix
    max_width = 0
    for row in M:
        for item in row:
            item_str = str(item)
            if len(item_str) > max_width:
                max_width = len(item_str)

    # Print each row with aligned columns
    for row in M:
        # Convert all elements to strings and format with padding
        formatted_row = [f" {str(item):>{max_width}} " for item in row]
        print("[" + "".join(formatted_row) + "]")

    if postfix_msg:
        print(postfix_msg)
    return M


def matrCmp(M1, M2):
    for i, row in enumerate(M1):
        for j in range(len(row)):
            if not M1[i][j] == M2[i][j]:
                return False
    return True


def CYK_graph(M, G=None, log=False):
    M_prev = copy.deepcopy(M)
    for i, row in enumerate(M):
        for j in range(len(row)):
            nonterm_list = search_lhs_terminal_rule(M[i][j])
            M[i][j] = nonterm_list

    if log == True:
        logM(M, "After 1st step:")

    n = len(M)
    for substring_length in range(2, len(M[0])):
        for i in range(n - substring_length):
            for first_len in range(1, substring_length):
                k = i + first_len
                j = i + substring_length
                first_non_term_set = M[i][k]
                second_non_term_set = M[k][j]

                for lhr in first_non_term_set:
                    for rhr in second_non_term_set:
                        ntr = search_lhs_non_terminal_rule(lhr, rhr, log)
                        if len(ntr) > 0:
                            s = set(M[i][j])
                            s.update(ntr)
                            M[i][j] = list(s)
        if log:
            logM(M, prefix_msg="M after current pass:")

if __name__ == "__main__":
    print("==========Test 1===========")
    # W = w_1, w_2, ... w_i, w_{i+1}, ... w_n
    # graph[i][j] is set of terminals which generate subword W^\prime = w_i, w_{i+1}, ... w_{j-1}
    # base case graph[0][1] = "a" graph[1][2] = "d" graph[2][3] = "d" graph[3][4] = "c"
    # I literally do not know why graph has 4th row
    # if word W can be generated = means that "S" in G[0][len(W)]
    graph1 = [
        ["0", "a", "0", "0", "0"],
        ["0", "0", "d", "0", "0"],
        ["0", "0", "0", "d", "0"],
        ["0", "0", "0", "0", "c"],
        ["0", "0", "0", "0", "0"],
    ]

    CYK_graph(graph1, G, True)
    print("==========Test 2===========")
    # now here we get extra terminal c in position graph[3][3]. I do not understand in the slightest
    graph2 = [
        ["0", "a", "0", "0", "0"],
        ["0", "0", "d", "0", "0"],
        ["0", "0", "0", "d", "0"],
        ["0", "0", "0", "c", "c"],
        ["0", "0", "0", "0", "0"],
    ]

    CYK_graph(graph2, G, True)
