import numpy as np
import networkx as nx

FILE = "day15_input.txt"


def get_input(file):
    with open(file, "r") as f:
        lines = f.read().strip("\n").split("\n")
    cols = len(lines[0])
    rows = len(lines)
    data = np.zeros((rows, cols), dtype=int)
    for i in range(rows):
        for j in range(cols):
            data[i, j] = lines[i][j]
    return data


def create_graph(data):
    G = nx.DiGraph()
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if j < data.shape[1] - 1:
                G.add_edge((i, j), (i, j + 1), weight=data[i, j + 1])
            if i < data.shape[0] - 1:
                G.add_edge((i, j), (i + 1, j), weight=data[i + 1, j])
            if i > 0:
                G.add_edge((i, j), (i - 1, j), weight=data[i - 1, j])
            if j > 0:
                G.add_edge((i, j), (i, j - 1), weight=data[i, j - 1])
    return G


def incr_tile(data):
    tile = data.copy()
    tile = tile + 1
    tile[tile > 9] = 1
    return tile


def grow_map(data, x_size=4, y_size=4):
    map = data.copy()
    tile = map.copy()
    for i in range(x_size):
        tile = incr_tile(tile)
        map = np.hstack([map, tile])
    tile = map.copy()
    for j in range(y_size):
        tile = incr_tile(tile)
        map = np.vstack([map, tile])
    return map


if __name__ == "__main__":
    data = get_input(FILE)

    # Part 1
    graph = create_graph(data)
    end = (data.shape[0] - 1, data.shape[1] - 1)
    shortest_length = nx.shortest_path_length(
        graph, source=(0, 0), target=end, weight="weight"
    )
    print("Part 1 answer:", shortest_length)

    # Part 2
    new_map = grow_map(data)
    end = (new_map.shape[0] - 1, new_map.shape[1] - 1)
    new_graph = create_graph(new_map)

    shortest_length = nx.shortest_path_length(
        new_graph, source=(0, 0), target=end, weight="weight"
    )
    print("Part 2 answer:", shortest_length)
