import numpy as np


def read_data(file):
    with open(file, "r") as f:
        content = f.read().strip("\n")
    data = content.split("\n")
    return data


def len_pos_diff(x):
    x_d = np.diff(x)
    return len(x_d[x_d > 0])


def win_calc(x, win_size=3):
    v = np.ones(win_size)
    x_window = np.convolve(x, v, "valid")
    return x_window


def calc_pos(data, h_pos=0, depth=0, aim=0):
    for line in data:
        cmd, val = line.split()
        if cmd == "forward":
            h_pos += int(val)
            depth += aim * int(val)
        elif cmd == "down":
            aim += int(val)
        elif cmd == "up":
            aim -= int(val)
    return h_pos, depth


data = read_data("day2_input.txt")

h_pos, depth = calc_pos(data)
print(f"Horizontal position: {h_pos}")
print(f"Depth: {depth}")
print(depth*h_pos)
