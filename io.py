"""
This module contains the file operations.
"""

import utils

INPUT_DIR = "inputs/"
INPUT_EXTENSION = ".in"


def read_configuration(input_instance):
    path = INPUT_DIR + input_instance + INPUT_EXTENSION

    unavailable_locations = []
    server_capacities = []
    server_slots = []

    with open(path) as file:
        for line_number, line in enumerate(file):
            if line_number == 0:
                rows, slots_per_row, unavailable_slots, pools, servers = utils.split_and_cast(line)
                unavailable_section_end = line_number + unavailable_slots
                server_section_start = unavailable_section_end + 1
            elif 1 <= line_number <= unavailable_section_end:
                unavailable_locations.append(utils.split_and_cast(line))
            elif line_number >= server_section_start:
                slots, capacity = utils.split_and_cast(line)
                server_slots.append(slots)
                server_capacities.append(capacity)

    return {"rows": rows,
            "slots_per_row": slots_per_row,
            "unavailable_slots": unavailable_slots,
            "pools": pools,
            "servers": servers,
            "unavailable_locations": unavailable_locations,
            "server_slots": server_slots,
            "server_capacities": server_capacities,
            "input_instance": input_instance}


def write_solution(solution, output_file="solution"):
    solution_as_string = ""

    for server_config in solution:
        if server_config["row"] is None:
            solution_as_string += "x"
        else:
            solution_as_string += " ".join([str(int_value) for int_value in
                                            [server_config["row"], server_config["slot"], server_config["pool"]]])

        solution_as_string += "\n"

    path = output_file + ".out"
    with open(path, "w") as file:
        file.write(solution_as_string)

    print "Solution for written on ", path
