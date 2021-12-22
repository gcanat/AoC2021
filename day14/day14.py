FILE = "day14_input.txt"
N_ITER = 40


def get_input(file):
    with open(file, "r") as f:
        lines = f.read().strip("\n").split("\n")
    template = lines[0]
    insertions = lines[2:]
    insert = {}
    for insertion in insertions:
        key = insertion.split(" -> ")[0]
        val = insertion.split(" -> ")[1]
        insert[key] = val
    return template, insert


def incr_letter(letter, dico, mult=1):
    if letter in dico.keys():
        dico[letter] += 1 * mult
    else:
        dico[letter] = 1 * mult
    return dico


def create_pairs(template):
    letter_count = {}
    pairs = {}
    for i in range(len(template) - 1):
        letter_count = incr_letter(template[i], letter_count)
        pair = template[i : i + 2]
        if pair in pairs.keys():
            pairs[pair] += 1
        else:
            pairs[pair] = 1
    letter_count = incr_letter(template[-1], letter_count)
    return pairs, letter_count


def insert_elem(pairs, insert, letter_count):
    updated_pairs = []
    new_pairs = {}
    # find which pairs are going to get splitted
    for insert_pair in insert.keys():
        if insert_pair in pairs.keys():
            updated_pairs.append(insert_pair)
            pair1 = insert_pair[0] + insert[insert_pair]
            pair2 = insert[insert_pair] + insert_pair[1]
            letter_count = incr_letter(
                insert[insert_pair], letter_count, pairs[insert_pair]
            )
            for x in (pair1, pair2):
                if x in new_pairs.keys():
                    new_pairs[x] += 1 * pairs[insert_pair]
                else:
                    new_pairs[x] = 1 * pairs[insert_pair]
    # pairs that didnt get split are kept with the same count
    for pair in pairs.keys():
        if pair not in updated_pairs:
            new_pairs[pair] = pairs[pair]
    return new_pairs, letter_count


def get_count(letter_count):
    count = sorted(letter_count.items(), key=lambda kv: -kv[1])
    return count


if __name__ == "__main__":
    template, insert = get_input(FILE)
    pairs, letter_count = create_pairs(template)
    for i in range(N_ITER):
        pairs, letter_count = insert_elem(pairs, insert, letter_count)
    count = get_count(letter_count)
    print(pairs)
    print(count)
    print(count[0], count[-1])
    print(f"Part 1 answer: {count[0][1] - count[-1][1]}")
