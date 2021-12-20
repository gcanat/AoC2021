import numpy as np

with open("day9_input.txt", "r") as f:
    lines = f.read().strip("\n").split("\n")

x = []
for line in lines:
    x.append(np.array([int(i) for i in line]))

x = np.vstack(x)
n = x.shape[0]
m = x.shape[1]

y = np.ones(x.shape[1]) * 99
y = y.reshape(1, -1)
z = np.ones(x.shape[0] + 2) * 99
z = z.reshape(-1, 1)

x = np.vstack([y, x, y])
x = np.hstack([z, x, z])

min_list = []

min_idx = []

for i in range(1, n + 1):
    for j in range(1, m + 1):
        if (
            (x[i, j] < x[i + 1, j])
            and (x[i, j] < x[i, j + 1])
            and (x[i, j] < x[i, j - 1])
            and (x[i, j] < x[i - 1, j])
        ):
            min_list.append(x[i, j])
            min_idx.append((i, j))

min_points = np.array(min_list, dtype=int)
risk = min_points + 1
tot_risk = np.sum(risk)
print(tot_risk)

basin = []


def explore_neigh(x, p_i, p_j, neigh_idx):
    # explore left
    if (
        (p_j > 1)
        and (x[p_i, p_j - 1] < 9)
        and (x[p_i, p_j - 1] >= x[p_i, p_j])
        and ((p_i, p_j - 1) not in neigh_idx)
    ):
        neigh_idx.append((p_i, p_j - 1))
        neigh_idx = explore_neigh(x, p_i, p_j - 1, neigh_idx)
    # explore right:
    if (
        (p_j < x.shape[1] - 1)
        and (x[p_i, p_j + 1] < 9)
        and (x[p_i, p_j + 1] >= x[p_i, p_j])
        and ((p_i, p_j + 1) not in neigh_idx)
    ):
        neigh_idx.append((p_i, p_j + 1))
        neigh_idx = explore_neigh(x, p_i, p_j + 1, neigh_idx)
    # explore up
    if (
        (p_i > 1)
        and (x[p_i - 1, p_j] < 9)
        and (x[p_i - 1, p_j] >= x[p_i, p_j])
        and ((p_i - 1, p_j) not in neigh_idx)
    ):
        neigh_idx.append((p_i - 1, p_j))
        neigh_idx = explore_neigh(x, p_i - 1, p_j, neigh_idx)
    # explore down
    if (
        (p_i < x.shape[0] - 1)
        and (x[p_i + 1, p_j] < 9)
        and (x[p_i + 1, p_j] >= x[p_i, p_j])
        and ((p_i + 1, p_j) not in neigh_idx)
    ):
        neigh_idx.append((p_i + 1, p_j))
        neigh_idx = explore_neigh(x, p_i + 1, p_j, neigh_idx)

    return neigh_idx


basin_sets = {}
basin_length = []
for idx in min_idx:
    print("exploring from starting point", idx)
    counter = 0
    for key in basin_sets:
        if basin_sets[key].intersection(idx) != set():
            counter += 1
    if counter != 0:
        continue
    basin_idx = explore_neigh(x, idx[0], idx[1], [idx])
    basin_set = set(basin_idx)
    counter = 0
    for key in basin_sets:
        if basin_sets[key].intersection(basin_set) != set():
            basin_sets.pop(key)
            counter += 1
    if counter == 0:
        basin_sets[idx] = basin_set
        basin_length.append(len(basin_set))


bas_len = np.array(basin_length, dtype=int)
big_bas = np.sort(bas_len)[-3:]
print(big_bas)
