import numpy as np

with open("day5_input.txt", "r") as f:
    content = f.read().strip("\n").split("\n")

# x[1], y[1] -> x[2], y[2]
diagram = np.zeros((1000, 1000), dtype=int)

for line in content:
    coord1, coord2 = line.split("->")
    coord1 = np.array(coord1.split(","), dtype=int)
    coord2 = np.array(coord2.split(","), dtype=int)
    x1, y1 = coord1[0], coord1[1]
    x2, y2 = coord2[0], coord2[1]
    if (x1 != x2) and (y1 != y2):
        x_size = np.abs(x2 - x1) + 1
        y_size = np.abs(y2 - y1) + 1
        conv = np.zeros((y_size, x_size), dtype=int)
        conv1 = conv + np.eye(y_size, dtype=int)
        conv2 = conv + np.fliplr(np.eye(y_size, dtype=int))
        if (x2 > x1) and (y2 > y1):
            diagram[y1 : y2 + 1, x1 : x2 + 1] += conv1
        elif (x2 > x1) and (y1 > y2):
            diagram[y2 : y1 + 1, x1 : x2 + 1] += conv2
        elif (x1 > x2) and (y1 > y2):
            diagram[y2 : y1 + 1, x2 : x1 + 1] += conv1
        elif (x1 > x2) and (y2 > y1):
            diagram[y1 : y2 + 1, x2 : x1 + 1] += conv2
    else:
        diff = coord2 - coord1
        if diff[0] != 0:
            x_start = min(x1, x2)
            x_stop = max(x1, x2) + 1
            diagram[y1, x_start:x_stop] += 1
        if diff[1] != 0:
            y_start = min(y1, y2)
            y_stop = max(y1, y2) + 1
            diagram[y_start:y_stop, x1] += 1
print(diagram[diagram >= 2].shape)
