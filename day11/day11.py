import numpy as np

FILE = "day11_input.txt"
N_STEPS = 100


def load_file(file):
    with open(file, "r") as f:
        lines = f.read().strip("\n").split("\n")

    matrix = []
    for line in lines:
        matrix.append([x for x in line])

    input = np.array(matrix, dtype=int)

    row_pad = np.ones(input.shape[1]) * -1
    input = np.vstack([row_pad, input, row_pad])

    col_pad = np.ones((input.shape[0], 1)) * -1
    input = np.hstack([col_pad, input, col_pad])
    return input


def step_next(x):
    flashed = np.zeros(x.shape, dtype=int)
    x[x > -1] += 1
    flashing = np.transpose(np.nonzero(x > 9))
    for i in range(len(flashing)):
        if flashed[flashing[i][0], flashing[i][1]] == 0:
            x, flashed = propagate(x, flashing[i], flashed)
    flash_count = np.sum(np.sum(flashed))
    return x, flash_count


def propagate(x, idx, flashed):
    i, j = idx[0], idx[1]
    flashed[i, j] = 1
    x[i, j] = 0
    # get the desired window
    i_min, i_max = i - 1, i + 2
    j_min, j_max = j - 1, j + 2
    # find all indexes to increment (ie not padded borders)
    idx_to_update = np.transpose(np.nonzero(x[i_min:i_max, j_min:j_max] > -1))
    a_flashed = flashed[i_min:i_max, j_min:j_max]

    for k in range(len(idx_to_update)):
        # check that it has not already flashed during this step
        if a_flashed[idx_to_update[k][0], idx_to_update[k][1]] == 0:
            i_upd = i - 1 + idx_to_update[k][0]
            j_upd = j - 1 + idx_to_update[k][1]
            x[i_upd, j_upd] += 1
            # propagate if value > 9 (DFS style)
            if x[i_upd, j_upd] > 9:
                x, flashed = propagate(x, (i_upd, j_upd), flashed)

    # find indices that will flash (BFS style)
    indices = np.transpose(np.nonzero(x[i_min:i_max, j_min:j_max] > 9))
    for k in range(len(indices)):
        new_i = i - 1 + indices[k][0]
        new_j = j - 1 + indices[k][1]
        if flashed[new_i, new_j] == 0:
            x, flashed = propagate(x, (new_i, new_j), flashed)

    return x, flashed


if __name__ == "__main__":
    input = load_file(FILE)
    total_flashes = 0
    # Part 1
    for i in range(N_STEPS):
        input, flash_count = step_next(input)
        # print(flash_count)
        total_flashes += flash_count

    print("Part 1 answer:", total_flashes)

    # Part 2
    flash_count = 0
    grid_size = (input.shape[0] - 2) * (input.shape[1] - 2)
    while flash_count != grid_size:
        input, flash_count = step_next(input)
        i += 1
    print(f"Part2, All synched at iter: {i+1}")
