import numpy as np

FILE = "day13_input.txt"


def get_input(file):
    with open(file, "r") as f:
        lines = f.read().strip("\n").split("\n")
    mapping = []
    folds = []
    for line in lines:
        if line.__contains__(","):
            coord = line.split(",")
            mapping.append(coord)
        elif line != "":
            fold_orient = line.split("=")[0][-1]
            fold_val = int(line.split("=")[1])
            folds.append((fold_orient, fold_val))
    mapping = np.array(mapping, dtype=int)
    return mapping, folds


def process_input(mapping, folds, part=1):
    maxes = np.max(mapping, axis=0)
    max_x, max_y = maxes[0], maxes[1]
    map_mat = np.zeros((max_y + 1, max_x + 1), dtype=int)
    for i in range(len(mapping)):
        map_mat[mapping[i][1], mapping[i][0]] = 1
    for fold in folds:
        print(map_mat.shape)
        fold_ax = fold[0]
        fold_val = fold[1]
        if fold_ax == "y":
            mat_up = map_mat[:fold_val, :]
            mat_down = map_mat[fold_val + 1 :, :]
            if mat_down.shape[0] < mat_up.shape[0]:
                pad_size = mat_up.shape[0] - mat_down.shape[0]
                pad = np.zeros((pad_size, mat_up.shape[1]))
                mat_down = np.vstack([mat_down, pad])
            mat_down = np.flipud(mat_down)
            mat_folded = mat_up + mat_down
        elif fold_ax == "x":
            mat_left = map_mat[:, :fold_val]
            mat_right = map_mat[:, fold_val + 1 :]
            if mat_right.shape[1] < mat_left.shape[1]:
                pad_size = mat_left.shape[1] - mat_right.shape[1]
                pad = np.zeros((mat_left.shape[0], pad_size))
                mat_right = np.hstack([mat_right, pad])
            mat_right = np.fliplr(mat_right)
            mat_folded = mat_left + mat_right
        if part == 1:
            break
        map_mat = mat_folded
    return map_mat


if __name__ == "__main__":
    mapping, folds = get_input(FILE)
    # part1
    mat_folded = process_input(mapping, folds)
    mask = mat_folded > 0
    print(np.sum(np.sum(mask)))
    # part 2
    mat_folded = process_input(mapping, folds, part=2)
    mask = mat_folded > 0
    mat_folded[mat_folded > 0] = 1
    output = ""
    for i in range(mat_folded.shape[0]):
        for j in range(mat_folded.shape[1]):
            if mat_folded[i, j] == 1:
                output += "8"
            else:
                output += " "
        output += "\n"
    print(output)
