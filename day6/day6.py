import numpy as np

NUM_ITER = 256

with open("day6_input.txt", "r") as f:
    numbers = f.read().strip("\n").split(",")

numbers = np.array(numbers, dtype=int)
_, counts = np.unique(numbers, return_counts=True)

num_children = np.zeros(NUM_ITER + 2)

# etat à l'iteration 0
counts = np.hstack([0, counts, 0])
print(counts)

for i in range(NUM_ITER):
    num_children[i + 2] = counts[0]
    counts = np.hstack([counts[1:7], counts[0] + num_children[i]])


# len_pop = []
# for i in range(len(numbers)):
#     number = numbers[i : i + 1].copy()
#     for day in range(256):
#         zero_idx = np.where(number == 0)[0]
#         number -= 1
#         number[zero_idx] = 6
#         curr_size = len(number)
#         kids_size = len(zero_idx)
#         number.resize(curr_size + kids_size)
#         number[curr_size:] = 8
#     len_pop.append(len(number))
#     del number


final_count = np.sum(counts) + num_children[NUM_ITER] + num_children[NUM_ITER+1]
print(final_count)
