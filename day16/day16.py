FILE = "day16_input.txt"


def get_input(file):
    with open(file, "r") as f:
        content = f.read().strip("\n")
    return content


hex_dict = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def hex2bin(hex_val):
    """Convert hexadecimal to binary, according to hex_dict"""
    bin_val = ""
    for x in hex_val:
        bin_val += hex_dict[x]
    return bin_val


def bin2dec(bin_val):
    """Convert binary to decimal"""
    max_power = len(bin_val)
    dec_val = 0
    i = 1
    for x in bin_val:
        dec_val += int(x) ** (max_power - i)
        i += 1
    return dec_val


def get_header(bin_val):
    """Parse packet header"""
    # print("getting header")
    bin_vers = bin_val[:3]
    bin_type = bin_val[3:6]
    dec_vers = bin2dec(bin_vers)
    dec_type = bin2dec(bin_type)
    return dec_vers, dec_type


def parse_literal_val(bin_val):
    """Parse literal value of type 4 packet"""
    # print("parsing literal")
    digit = ""
    digit_length = 6
    i = 6
    while True:
        digit_length += 5
        # group = bin_val[i: i + 5]
        digit += str(bin2dec(bin_val[i + 1 : i + 5]))
        if bin_val[i] == "0":
            break
        i += 5
    while (digit_length % 4) != 0:
        digit_length += 1
    return digit, digit_length


def process_bin(bin_val):
    print("processing binary")
    all_vers = []
    dec_vers, dec_type = get_header(bin_val)
    all_vers.append(dec_vers)
    len_count = 0
    if dec_type == 4:
        print("found literal inside processing bin")
        digit, digit_length = parse_literal_val(bin_val)
        len_count += digit_length
    else:
        print("found operator inside processing bin")
        operator, op_length, sub_vers = parse_operator(bin_val)
        len_count += op_length
        all_vers += sub_vers
    return len_count, all_vers


def parse_operator(bin_val):
    """Parse other types of packets"""
    all_vers = []
    operator = None
    # print(f"parsing operator {len(bin_val)}", end="\r")
    # if len(bin_val) < 6:
    #     return None, len(bin_val), []
    pack_len = 7
    len_count = 0
    print("subpacket type", bin_val[6], type(bin_val[6]))
    if bin_val[6] == "0":
        # find next 15 bits
        pack_len += 15
        sub_pack_len = bin2dec(bin_val[7:22])
        while len_count < sub_pack_len:
            dec_vers, dec_type = get_header(bin_val[22 + len_count :])
            all_vers.append(dec_vers)
            if dec_type == 4:
                # print("cond 1")
                digit, digit_length = parse_literal_val(bin_val[22 + len_count :])
                len_count += digit_length
            else:
                # print("cond 2")
                operator, op_length, sub_vers = parse_operator(
                    bin_val[22 + len_count :]
                )
                len_count += op_length
                all_vers += sub_vers
    elif bin_val[6] == "1":
        # find number of subpackets contained
        pack_len += 11
        subpack_num = bin2dec(bin_val[7:18])
        subpack_counter = 0
        print("cond 3")
        print("subpack_num", subpack_num, " len bin_val", len(bin_val))
        for _ in range(subpack_num):
            print("subpack_counter", subpack_counter, "subpack_num", subpack_num)
            dec_vers, dec_type = get_header(bin_val[18 + len_count :])
            all_vers.append(dec_vers)
            if dec_type == 4:
                print("cond 4")
                digit, digit_length = parse_literal_val(bin_val[18 + len_count :])
                len_count += digit_length
                subpack_counter += 1
            else:
                print("cond 5")
                operator, op_length, sub_vers = parse_operator(
                    bin_val[18 + len_count :]
                )
                len_count += op_length
                # print("length count", len_count, " len bin_val", len(bin_val))
                all_vers += sub_vers
                subpack_counter += 1
    return operator, pack_len + len_count, all_vers


if __name__ == "__main__":
    hex_content = get_input(FILE)
    bin_content = hex2bin(hex_content)
    len_count = 0
    all_vers = []
    while len_count < len(bin_content):
        print(f"{len_count}\r")
        operator, curr_len, curr_vers = process_bin(bin_content[len_count:])
        len_count += curr_len
        all_vers += curr_vers

    print(sum(curr_vers))
