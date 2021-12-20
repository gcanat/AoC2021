import numpy as np


def len_pos_diff(x):
    x_d = np.diff(x)
    print(len(x_d[x_d > 0]))


with open("day1_input.txt", "r") as f:
    content = f.read().strip("\n")

x = np.array(content.split("\n"), dtype=int)
len_pos_diff(x)

v = np.ones(3)
x_window = np.convolve(x, v, "valid")
len_pos_diff(x_window)
