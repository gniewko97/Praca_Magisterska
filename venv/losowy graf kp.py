import random
from pathlib import Path


def generate_tree_from_prufer_code(code):
    L1 = {}
    L2 = []
    edges = []

    for node in range(len(code)+2):
        L2.append(node+1)
    for node in L2:
        L1[node] = 0
    for node in code:
        L1[node] += 1

    for k in range(len(L1)):
        current_node = L2[0]
        counter = 1
        if len(L2) > 2:
            while L1[current_node] > 0:
                current_node = L2[counter]
                counter += 1
            if code[k] < current_node:
                edges.append([code[k], current_node])
            else:
                edges.append([current_node, code[k]])
            L1[code[k]] -= 1
            L2.remove(current_node)
    edges.append([L2[0], L2[1]])
    return edges


def generate_prufers_code(n: int):
    code = []
    for i in range(n-2):
        code.append(random.randint(1, n))
    return code


def generate_random_graph(n: int, edges_number: int, log=False):
    code = generate_prufers_code(n)
    edges = generate_tree_from_prufer_code(code)
    edges_dict = {}
    for index in range(len(edges)):
        edges_dict[(edges[index][0], edges[index][1])] = True
    while len(edges_dict) < edges_number:
        node1 = random.randint(1, n)
        node2 = random.randint(1, n)
        while node1 == node2:
            node2 = random.randint(1, n)
        if node1 < node2:
            edges_dict[(node1, node2)] = True
        else:
            if [node2, node1] not in edges:
                edges_dict[(node2, node1)] = True
    return edges_dict.keys()


def write_graph_to_file(graph, ilosc, filename, path="grafy/"):
    with open(path + filename, 'w') as file:
        file.write(str(ilosc) + "\n")
        for edge in graph:
            weight = random.randint(1, 100)
            file.write(str(edge[0]) + ", " + str(edge[1]) + ", " + str(weight) + "\n")


def read_graph_from_file(filename, path="grafy/"):
    N = set()
    A = {}
    A_b = {}
    w = {}

    with open(path + filename, 'r') as file:
        line = file.readline()
        while line != '':
            split = line.strip('\n').split(" ")

            first_node = int(split[0])
            second_node = int(split[1])

            N.add(first_node)
            N.add(second_node)

            if first_node not in A.keys():
                A[first_node] = [second_node]
            else:
                A[first_node].append(second_node)

            if second_node not in A_b.keys():
                A_b[second_node] = [first_node]
            else:
                A_b[second_node].append(first_node)

            w[(first_node, second_node)] = int(split[2])

            line = file.readline()
    return N, A, A_b, w


if __name__ == '__main__':
    n = [200, 500, 1_000, 2_000, 5_000, 10_000]
    for k in [3, 5]:
        group = str(k) + "n"
        print("generuje grafy z grupy:", str(k) + "n")
        for i in range(1, len(n)+1):
            print("generuje grafy z grupy:", group, "z", n[i - 1], "wierzchołkami i", int(k * n[i - 1]), "krawędziami")
            p = "grafy/" + group + "/" + str(n[i-1]) + "/"
            for j in range(1, 51):
                print("graf:", j, "z", 50)
                g = generate_random_graph(n[i-1], int(k * n[i - 1]), log=True)
                f = "graf" + str(j)
                l = n[i - 1]
                Path(p).mkdir(parents=True, exist_ok=True)
                write_graph_to_file(g, l, f, p)
            print()
