from operator import mul
import functools
from typing import List


def mult(values: List[int]) -> int:  # Multiply list of literal values
    return functools.reduce(mul, values, 1)


def gt(values: List[int]) -> int:
    if values[0] > values[1]:
        return 1
    else:
        return 0


def lt(values: List[int]) -> int:
    if values[0] < values[1]:
        return 1
    else:
        return 0


def eq(values: List[int]) -> int:
    if values[0] == values[1]:
        return 1
    else:
        return 0


# Hexadecimal to binary.
def hex_to_bin(hex_data: str) -> str:
    total_bin_bit_size = (
        len(hex_data) * 4
    )  # Each hexadecimal corresponds to 4 bits of binary data.
    # Needs to convert hex_input to integer before converting to binary. Removes leading 0b.
    # Fills with starting zeros until the bit size equals that of total_bin_bit_size
    bin_data = bin(int(hex_data, base=16))[2:].zfill(total_bin_bit_size)

    return bin_data


# Binary data to int
def bin_to_int(bin_data: str) -> int:
    return int(bin_data, 2)


# Reads header, returning version number and packet type ID.
def read_header(packet: str) -> (int, int):
    return bin_to_int(packet[0:3]), bin_to_int(packet[3:6])


# Used recursively, mostly. Stores literal values in list 'values'.
def read_packet(packet: str) -> (int, str):
    # Function placed inside parse_packet() to keep list_value_list in correct scope.
    def parse_operator_packet(packet):
        length_type_id, packet = bin_to_int(packet[0]), packet[1:]

        if (
            length_type_id == 0
        ):  # 15 bits after length_type_id represents the subpacket's size in bits
            length_size = 15  # The number of following bits which represent the packet's body's size in number of bits.
            packet_size_bits, packet = (
                bin_to_int(packet[0:length_size]),
                packet[length_size:],
            )  # Subpacket's size in bits
            subpacket, packet = packet[0:packet_size_bits], packet[packet_size_bits:]

            while subpacket:  # Until a subpacket isn't returned.
                value, subpacket = read_packet(subpacket)
                values.append(value)

        elif (
            length_type_id == 1
        ):  # 11 bits after length_type_id represents the subpacket's size in subpackets.
            length_size = 11  # Following bits which represent the packet's body's size in number of subpackets.
            packet_size_subpackets, packet = (
                bin_to_int(packet[0:length_size]),
                packet[length_size:],
            )

            for _ in range(
                packet_size_subpackets
            ):  # For number of subpackets which make up the packet.
                value, packet = read_packet(packet)
                values.append(value)

        return packet

    (version, type_id), packet = read_header(packet), packet[6:]
    versions.append(version)

    if type_id == 4:
        value, packet = parse_literal_packet(packet)
    else:
        values = []
        packet = parse_operator_packet(packet)  # Saves values in list 'values'
        if type_id == 0:
            value = sum(values)
        elif type_id == 1:
            value = mult(values)
        elif type_id == 2:
            value = min(values)
        elif type_id == 3:
            value = max(values)
        elif type_id == 5:
            value = gt(values)
        elif type_id == 6:
            value = lt(values)
        elif type_id == 7:
            value = eq(values)

    return value, packet


# Parses and reads literal packet. Returns literal value and rest of packet.
def parse_literal_packet(packet: str) -> (int, str):
    bits_per_subpacket = 5
    packet_lit_val_bin = (
        ""  # To store the parsed literal value of the packet in binary form
    )

    subpacket_number = 1
    while True:  # Parsing and reading each subpacket until finding last one.
        lower_limit = (subpacket_number - 1) * bits_per_subpacket
        upper_limit = subpacket_number * bits_per_subpacket
        subpacket = packet[lower_limit:upper_limit]
        packet_lit_val_bin += subpacket[
            1:bits_per_subpacket
        ]  # 0th bit indicates if it's the last subpacket or not

        if (
            bin_to_int(subpacket[0]) == 0
        ):  # Indicates that subpacket is last packet's body.
            num_of_subpackets = subpacket_number  # Total number of subpackets
            break
        subpacket_number += 1

    bits_read = (
        num_of_subpackets * bits_per_subpacket
    )  # The total size in bits of the body of the literal packet
    lit_val = bin_to_int(packet_lit_val_bin)

    return lit_val, packet[bits_read:]


# Read the hexadecimal transmission
def read_transmission(hex_data: str) -> (int, int):
    versions.clear()  # In case read_transmission() is to be run more than once.
    packet = hex_to_bin(hex_data)
    value, _ = read_packet(packet)  # Only the resulting value is of use at this level.
    sum_versions = sum(versions)

    return sum_versions, value


if __name__ == "__main__":
    versions = []  # Global variable to collect all the version numbers.
    with open("day16_input.txt", "r") as f:
        content = f.read().strip("\n")
    sum_versions, value = read_transmission(content)
    print(f"Sum of versions is {sum_versions} and value is {value}")
