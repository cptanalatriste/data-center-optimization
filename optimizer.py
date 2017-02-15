"""
Optimization algorithms
"""
import io
import random

import utils


def mutate_solution(solution, supported_pools):
    server_index = random.randint(0, len(solution) - 1)
    current_pool = solution[server_index]

    direction = random.random()

    mutated_solution = list(solution)
    if direction < 0.5 and current_pool > 0 and mutated_solution[server_index] is not None:
        mutated_solution[server_index] -= 1
    elif current_pool < supported_pools - 1 and mutated_solution[server_index] is not None:
        mutated_solution[server_index] += 1

    return mutated_solution


def apply_crossover(solution, another_solution):
    single_point = random.randint(1, len(solution) - 2)
    return solution[0: single_point] + another_solution[single_point:]


def genetic_optimizer(servers, supported_pools, input_instance, elite_ratio=0.2, population_size=50, iterations=1000,
                      mutation_probability=0.2):
    population = []

    for _ in range(population_size):
        individual = [random.randint(0, supported_pools - 1) if server.allocated() else None
                      for server in servers]
        population.append(individual)

    elite_size = int(elite_ratio * population_size)
    for _ in range(iterations):
        results = [(utils.apply_assignment(servers, supported_pools, individual), individual) for individual in
                   population]
        results.sort(reverse=True, key=lambda result: result[0][0])

        best_result = results[0]
        best_score = best_result[0][0]
        best_allocation = best_result[0][1]
        print "Best score on population: ", best_score
        # print " best allocation: ", best_allocation
        io.write_solution(best_allocation, output_file=input_instance)

        individuals_ranked = [individual for (results, individual) in results]
        # print "individuals_ranked ", individuals_ranked

        population = individuals_ranked[0: elite_size]

        while len(population) < population_size:
            if random.random() < mutation_probability:
                individual_to_mutate = individuals_ranked[random.randint(0, elite_size)]
                population.append(mutate_solution(individual_to_mutate, supported_pools))
            else:
                individual_for_crossover = individuals_ranked[random.randint(0, elite_size)]
                another_individual = individuals_ranked[random.randint(0, elite_size)]
                population.append(apply_crossover(individual_for_crossover, another_individual))

    return best_score, best_allocation


def hill_climbing_optimizer(servers, pools, current_solution=None, input_instance="solution"):
    if current_solution is None:
        current_solution = [random.randint(0, pools - 1) if server.allocated() else None
                            for server in servers]
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
