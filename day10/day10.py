import numpy as np


with open("day10_input.txt", "r") as f:
    lines = f.read().strip("\n").split("\n")

openings = ["(", "{", "<", "["]
closings = [")", "}", ">", "]"]

close_map = {")": "(", "}": "{", ">": "<", "]": "["}
open_map = {"(": ")", "{": "}", "<": ">", "[": "]"}

points = {")": 3, "]": 57, "}": 1197, ">": 25137}


chnk_cnt = dict(zip(openings + closings, [0] * len(openings + closings)))

op_count = 0
cl_count = 0
tot_points = 0

wait_list = []
inc_lines = []

for line in lines:
    i = 0
    for char in line:
        if char in openings:
            wait_list.append(open_map[char])
            i += 1
        if char in closings:
            i += 1
            if char == wait_list[-1]:
                wait_list.pop()
            else:
                tot_points += points[char]
                break
    if i == len(line):
        inc_lines.append(line)

print(tot_points)

scoring = {")": 1, "]": 2, "}": 3, ">": 4}
wait_list = []

scores = np.zeros(len(inc_lines), dtype=int)

for i, line in enumerate(inc_lines):
    local_score = 0
    wait_list = []
    for char in line:
        if char in openings:
            wait_list.append(open_map[char])
        elif char in closings:
            if char == wait_list[-1]:
                wait_list.pop()
    wait_list.reverse()
    for char in wait_list:
        local_score = (local_score * 5) + scoring[char]
        line += char
    scores[i] = local_score

print(len(scores))
print(np.median(scores))
