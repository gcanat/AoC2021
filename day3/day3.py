import numpy as np


def read_data(file):
    with open(file, "r") as f:
        content = f.read().strip("\n")
    data = content.split("\n")
    return data


data = read_data("day3_input.txt")

arr = []
for line in data:
    arr.append([x for x in line])

bin_mat = np.array(arr, dtype=int)


def filter_bins(bin_mat, type="most"):
    """Find the filter depending on type `most` or `least`"""
    means = np.mean(bin_mat, axis=0)
    means[means == 0.5] = 0.51
    filtered = np.round(means).astype(int)
    if type == "least":
        filtered = np.abs(filtered - 1)
    return filtered


def gen_bins(filtered):
    """Generate binary mask to convert to decimal"""
    bins = np.array([2 ** i for i in range(len(filtered) - 1, -1, -1)])
    return bins


def get_decimal(filtered):
    """Convert to decimal by doing a dot product with the binary mask"""
    bins = gen_bins(filtered)
    filtered_dec = np.dot(filtered, bins)
    return filtered_dec


gamma_dec = get_decimal(filter_bins(bin_mat))
epsilon_dec = get_decimal(filter_bins(bin_mat, type="least"))

print(f"gamma rate: {gamma_dec}")
print(f"espilon rate: {epsilon_dec}")
print(f"power consumption: {gamma_dec*epsilon_dec}")


def get_rating(bin_mat, type="o2"):
    """
    Find `oxygen generator rating` or `CO2 scrubber rating`
    ----
    Parameters:
    ----
    bin_mat : matrice of binary values
    type : one of `o2` or `co2`
    ----
    Return:
    ----
    decimal value of the found rating
    """
    n = bin_mat.shape[1]
    if type == "o2":
        filter_type = "most"
    else:
        filter_type = "least"

    reduced = bin_mat.copy()

    for i in range(n):
        filter = filter_bins(reduced, type=filter_type)
        reduced = reduced[reduced[:, i] == filter[i]]
        if len(reduced) == 1:
            bins = gen_bins(reduced.squeeze())
            num = np.dot(reduced, bins)
            print("found rating number", num)
            return num


o2_ratio = get_rating(bin_mat, type="o2")
co2_scrub = get_rating(bin_mat, type="co2")

print(f"Life support rating: {o2_ratio * co2_scrub}")
