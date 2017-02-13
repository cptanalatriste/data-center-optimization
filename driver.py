"""
This module coordinates the execution
"""
import domain
import io
import test


def allocate_servers(data_center, servers):
    for server in servers:
        if data_center.allocate(server) is None:
            print "Server ", server.id, " with ", server.capacity, " capacity couldn't be allocated."


def egalitarian_pool_assignment(servers, pools):
    allocated_servers = [server for server in servers if server.allocated()]

    servers_per_pool = len(allocated_servers) / pools

    print "Each of ", pools, " pools will have ", servers_per_pool, " servers from ", len(
        allocated_servers), " allocated servers."

    current_pool = 0
    pool_counter = 0

    for allocate_server in allocated_servers:
        allocate_server.pool = current_pool
        pool_counter += 1

        if pool_counter >= servers_per_pool:
            current_pool += 1
            pool_counter = 0


def manage_datacenter(problem_configuration):
    data_center, servers = domain.get_domain_objects(problem_configuration)

    allocate_servers(data_center, servers)
    egalitarian_pool_assignment(servers, data_center.pools)

    print "data_center ", data_center
    print "servers ", servers

    return [server.get_allocation_info() for server in servers]


def main():
    input_instance = "sample_input"

    problem_configuration = io.read_configuration(input_instance)
    print "problem_configuration: ", problem_configuration

    solution = manage_datacenter(problem_configuration)
    io.write_solution(solution, input_instance)


if __name__ == "__main__":
    main()
