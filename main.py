#!/usr/bin/env python3
import sys
import collections

class Edge:
    def __init__(self, to, rev, cap):
        self.to = to
        self.rev = rev
        self.cap = cap

def add_edge(G, u, v, cap):
    G[u].append(Edge(v, len(G[v]), cap))
    G[v].append(Edge(u, len(G[u]) - 1, 0))

def bfs(G, s, t, parent):
    n = len(G)
    visited = [False] * n
    queue = collections.deque([s])
    visited[s] = True
    parent[s] = (-1, -1)
    while queue:
        u = queue.popleft()
        for idx, e in enumerate(G[u]):
            if not visited[e.to] and e.cap > 0:
                visited[e.to] = True
                parent[e.to] = (u, idx)
                if e.to == t:
                    return True
                queue.append(e.to)
    return False

def max_flow(G, s, t):
    flow = 0
    n = len(G)
    parent = [(-1, -1)] * n
    while bfs(G, s, t, parent):
        path_flow = float('inf')
        v = t
        while v != s:
            u, idx = parent[v]
            path_flow = min(path_flow, G[u][idx].cap)
            v = u
        v = t
        while v != s:
            u, idx = parent[v]
            e = G[u][idx]
            re = G[e.to][e.rev]
            e.cap -= path_flow
            re.cap += path_flow
            v = u
        flow += path_flow
    return flow

def main():
    if len(sys.argv) != 3:
        print("Usage: python solver_survey.py INPUT_FILE OUTPUT_FILE")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file) as f:
        lines = f.read().strip().splitlines()
    header = list(map(int, lines[0].split()))
    C, P = header[0], header[1]

    l = [0]*C
    u = [0]*C
    can_review = [None]*C
    for i in range(C):
        parts = list(map(int, lines[1 + i].split()))
        l[i], u[i] = parts[0], parts[1]
        can_review[i] = parts[2:]
    demands = list(map(int, lines[1 + C].split()))
    v = demands

    S = 0
    cust_offset = 1
    prod_offset = cust_offset + C
    T = prod_offset + P
    SS = T + 1
    TT = SS + 1
    N = TT + 1

    G = [[] for _ in range(N)]
    b = [0] * N

    for i in range(C):
        u_node = S
        v_node = cust_offset + i
        low, up = l[i], u[i]
        add_edge(G, u_node, v_node, up - low)
        b[u_node] -= low
        b[v_node] += low

    assignment_edges = []
    for i in range(C):
        u_node = cust_offset + i
        for pj in can_review[i]:
            j = pj - 1
            v_node = prod_offset + j
            edge_idx = len(G[u_node])
            add_edge(G, u_node, v_node, 1)
            assignment_edges.append((u_node, edge_idx, j))

    for j in range(P):
        u_node = prod_offset + j
        v_node = T
        low, up = v[j], C
        add_edge(G, u_node, v_node, up - low)
        b[u_node] -= low
        b[v_node] += low

    sum_pos = 0
    for i in range(N):
        if b[i] > 0:
            add_edge(G, SS, i, b[i])
            sum_pos += b[i]
        elif b[i] < 0:
            add_edge(G, i, TT, -b[i])

    INF = sum(u) + sum(v) + C + 1
    idx_T_to_S = len(G[T])
    add_edge(G, T, S, INF)

    flow1 = max_flow(G, SS, TT)
    if flow1 != sum_pos:
        with open(output_file, 'w') as f:
            f.write("-1\n")
        return

    G[T][idx_T_to_S].cap = 0
    rev_idx = G[T][idx_T_to_S].rev
    G[S][rev_idx].cap = 0

    max_flow(G, S, T)

    assignments = [[] for _ in range(C)]
    for u_node, edge_idx, j in assignment_edges:
        e = G[u_node][edge_idx]
        if e.cap == 0:
            cust_i = u_node - cust_offset
            assignments[cust_i].append(j + 1)

    with open(output_file, 'w') as f:
        for i in range(C):
            if assignments[i]:
                f.write(" ".join(map(str, assignments[i])) + "\n")
            else:
                f.write("\n")

if __name__ == "__main__":
    main()

