with open("day8_input.txt", "r") as f:
    lines = f.read().strip("\n").split("\n")

counter = 0
for line in lines:
    x = line.split(" | ")
    for digit in x[1].split():
        if (
            (len(digit) == 2)
            or (len(digit) == 3)
            or (len(digit) == 4)
            or (len(digit) == 7)
        ):
            counter += 1

print("Part 1 answer:", counter)

segment = set(["a", "b", "c", "d", "e", "f", "g"])

seg_map = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}


mapping = {"a": None, "b": None, "c": None, "d": None, "e": None, "f": None, "g": None}


all_outputs = []
counter = 0
for line in lines:
    x = line.split(" | ")
    digits = x[0].split()
    words = {}
    for digit in digits:
        word_len = len(digit)
        if word_len in words.keys():
            words[word_len] += [digit]
        else:
            words[word_len] = [digit]

    letters1 = set([w for w in words[2][0]])

    for w in words[6]:
        letters6 = set([char for char in w])
        intersec = letters6.intersection(letters1)
        if len(intersec) == 1:
            mapping["c"] = letters1 - intersec

    mapping["f"] = letters1 - mapping["c"]

    letters7 = set([w for w in words[3][0]])
    mapping["a"] = letters7 - letters1

    # find 'g' because it's in 3 but not in (4 u 7)
    # 1st : find 3
    for w in words[5]:
        letters5 = set([char for char in w])
        known_letters = mapping["a"].union(mapping["c"]).union(mapping["f"])
        if known_letters - letters5 == set():
            d_g = letters5 - known_letters
    # 2nd : find 4
    letters4 = set([w for w in words[4][0]])
    mapping["d"] = d_g.intersection(letters4)
    mapping["g"] = d_g - mapping["d"]
    mapping["b"] = letters4 - mapping["c"] - mapping["d"] - mapping["f"]
    mapping["e"] = (
        segment
        - mapping["a"]
        - mapping["b"]
        - mapping["c"]
        - mapping["d"]
        - mapping["f"]
        - mapping["g"]
    )

    reverse_map = {}
    for key in mapping.keys():
        for i in mapping[key]:
            reverse_map[i] = key

    # process output
    outputs = x[1].split()
    output_value = ""
    for output in outputs:
        decrypted_segment = ""
        for char in output:
            decrypted_segment += reverse_map[char]
        for key in seg_map.keys():
            if set(decrypted_segment) == set(key):
                output_value += str(seg_map[key])
    counter += 1
    all_outputs.append(int(output_value))

print("Part 2 answer", sum(all_outputs))
