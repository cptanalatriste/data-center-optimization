"""
General purpose functions
"""


def split_and_cast(line):
    return [int(string_value) for string_value in line.split(" ")]
