"""
Domain objects for the problem
"""

import numpy as np

UNAVAILABLE = -1


class Server:
    def __init__(self, slots, capacity, id):
        self.id = id
        self.slots = slots
        self.capacity = capacity
        self.pool = None
        self.row = None
        self.slot = None

    def allocated(self):
        return self.row is not None

    def get_allocation_info(self):
        if not self.allocated():
            return {"row": None,
                    "slot": None,
                    "pool": None}

        return {"row": self.row,
                "slot": self.slot,
                "pool": self.pool}


class DataCenter:
    def __init__(self, unavailable_slots, rows, slots_per_row, pools, unavailable_locations):
        self.unavailable_slots = unavailable_slots
        self.rows = rows
        self.slots_per_row = slots_per_row
        self.pools = pools
        self.unavailable_locations = unavailable_locations
        self.row_catalog = [None] * self.rows

        print "slots_per_row ", type(slots_per_row), slots_per_row

        self.init_row_catalog()

    def init_row_catalog(self):
        for index, _ in enumerate(self.row_catalog):
            self.row_catalog[index] = [None] * self.slots_per_row

        for location in self.unavailable_locations:
            row, slot = location
            self.row_catalog[row][slot] = UNAVAILABLE

    def allocate(self, server):
        server_counts = [(index, len(set(row))) for index, row in enumerate(self.row_catalog)]
        server_counts.sort(key=lambda row_count: row_count[1])

        for row_index, _ in server_counts:
            row_slot = self.allocate_at_row(server, row_index)

            if row_slot is not None:
                print "Server ", server.id, " with ", server.slots, " slots allocated at row ", row_index, " at slot ", row_slot
                return row_index

        return None

    def allocate_at_row(self, server, row_index):
        candidate_row = self.row_catalog[row_index]

        for slot_index, server_in_place in enumerate(candidate_row):
            if server_in_place is None:
                current_slot = slot_index + 1
                while current_slot < len(candidate_row) and candidate_row[current_slot] is None:
                    current_slot += 1

                available_slots = current_slot - slot_index
                print "available_slots ", available_slots, " current_slot ", current_slot

                if available_slots >= server.slots:
                    server.row = row_index
                    server.slot = slot_index

                    last_index = slot_index + server.slots

                    for slot_in_row in range(slot_index, last_index):
                        candidate_row[slot_in_row] = server.id

                    return slot_index

        return None


def get_domain_objects(problem_configuration):
    unavailable_slots = problem_configuration["unavailable_slots"]
    rows = problem_configuration["rows"]
    slots_per_row = problem_configuration["slots_per_row"]
    pools = problem_configuration["pools"]
    unavailable_locations = problem_configuration["unavailable_locations"]

    data_center = DataCenter(unavailable_slots=unavailable_slots, rows=rows, slots_per_row=slots_per_row, pools=pools,
                             unavailable_locations=unavailable_locations)

    servers = []
    server_number = problem_configuration["servers"]
    for server_index in range(server_number):
        slots = problem_configuration["server_slots"][server_index]
        capacity = problem_configuration["server_capacities"][server_index]
        servers.append(Server(slots=slots, capacity=capacity, id=server_index))

    return data_center, servers
