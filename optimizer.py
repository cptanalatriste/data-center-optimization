"""
Optimization algorithms
"""
import io
import random

import utils


def hill_climbing_optimizer(servers, pools, input_instance="solution"):
    # random.seed(9001)

    current_solution = [random.randint(0, pools - 1) if server.allocated() else None for server in servers]
    # print "current_solution ", current_solution
    current_score, current_allocation = utils.apply_assignment(servers, pools, current_solution)
    print "current_score ", current_score
    io.write_solution(current_allocation, output_file=input_instance)

    while True:
        print "Locating neighbours ..."
        neighbors = []

        for server_index in range(len(current_solution)):
            current_pool = current_solution[server_index]

            if current_pool < pools - 1 and current_solution[server_index] is not None:
                neighbor = list(current_solution)
                neighbor[server_index] += 1
                neighbors.append(neighbor)

            if current_pool > 0 and current_solution[server_index] is not None:
                neighbor = list(current_solution)
                neighbor[server_index] -= 1
                neighbors.append(neighbor)

        print "Neighbours found: ", len(neighbors)
        better_found = False
        for neighbor in neighbors:
            neighbour_score, neighbour_allocation = utils.apply_assignment(servers, pools, neighbor)

            # print "neighbour_score ", neighbour_score
            if neighbour_score > current_score:
                print "Improvement found! Going to ", neighbour_score, " from ", current_score

                current_score = neighbour_score
                current_solution = neighbor
                current_allocation = neighbour_allocation

                better_found = True
                io.write_solution(current_allocation, output_file=input_instance)

        if not better_found:
            break

    return current_score, current_allocation
