"""
General purpose functions
"""
import sys


def split_and_cast(line):
    return [int(string_value) for string_value in line.split(" ")]


def get_allocation_results(servers, pools):
    solution = [server.get_allocation_info() for server in servers]
    pool_catalog = []

    for pool_index in range(pools):
        servers_in_pool = [server for server in servers if server.pool == pool_index]
        # print "pool ", pool_index, " has ", len(servers_in_pool), " servers."
        pool_catalog.append(servers_in_pool)

    score = min([get_pool_score(pool_servers) for pool_servers in pool_catalog])
    return score, solution


def get_pool_score(servers):
    rows_in_pool = set([server.row for server in servers])
    minimum_capacity = sys.maxint

    for row in rows_in_pool:
        capacity = 0
        for server in servers:
            if server.row != row:
                capacity += server.capacity

        if capacity < minimum_capacity:
            minimum_capacity = capacity

    return minimum_capacity


def assign_pools(servers, pools):
    for server_index, pool in enumerate(pools):
        if pool is not None:
            servers[server_index].pool = pool


def apply_assignment(servers, pools, pool_asignment):
    assign_pools(servers, pool_asignment)
    return get_allocation_results(servers, pools)
