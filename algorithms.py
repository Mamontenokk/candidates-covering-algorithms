import numpy as np
import random


def first_greedy_algorithm(candidates, present=[0]):
    
    result = present
    if len(result) == 1:
        present_groups = np.where(candidates[present[0],:] == 1)[0]
    else:
        present_groups = np.empty(shape=(0,1))
        for elem in result:
            covered_groups = np.where(candidates[elem,:] == 1)[0]
            unique_covered_groups = list(filter(lambda x: x not in present_groups, covered_groups))
            present_groups = np.append(present_groups, unique_covered_groups)
            
    while len(present_groups) != candidates.shape[1]:
        max_index = 0
        max_uncovered = []
        
        for candidate_index in filter(lambda x: x not in result, range(candidates.shape[0])):
            covered_groups = np.where(candidates[candidate_index,:] == 1)[0]
            unique_covered_groups = list(filter(lambda x: x not in present_groups, covered_groups))
            if len(unique_covered_groups) > len(max_uncovered):
                max_index = candidate_index
                max_uncovered = unique_covered_groups
        result.append(max_index)
        present_groups = np.append(present_groups, max_uncovered)
        
    return result


def second_greedy_algorithm(candidates, present=[0]):
    
    result = present
    if len(result) == 1:
        present_groups = np.where(candidates[present[0],:] == 1)[0]
    else:
        present_groups = np.empty(shape=(0,1))
        for elem in result:
            covered_groups = np.where(candidates[elem,:] == 1)[0]
            unique_covered_groups = list(filter(lambda x: x not in present_groups, covered_groups))
            present_groups = np.append(present_groups, unique_covered_groups)
    
    for group in range(candidates.shape[1]):
        if group in present_groups:
            continue
        else:
            for candidate_index in filter(lambda x: x not in result, range(candidates.shape[0])):
                covered_groups = np.where(candidates[candidate_index,:] == 1)[0]
                if group in covered_groups:
                    unique_covered_groups = list(filter(lambda x: x not in present_groups, covered_groups))
                    present_groups = np.append(present_groups, unique_covered_groups)
                    result.append(candidate_index)
                    break
                    
    return result


def third_greedy_algorithm(candidates, present = []):
    
    result = present
    present_groups = np.empty(shape=(0,1))
    if len(result) > 0:
        for elem in result:
            covered_groups = np.where(candidates[elem,:] == 1)[0]
            unique_covered_groups = list(filter(lambda x: x not in present_groups, covered_groups))
            present_groups = np.append(present_groups, unique_covered_groups)
    
    for candidate in filter(lambda x: x not in result, range(candidates.shape[0])):
        for candidate_index in filter(lambda x: x not in result, range(candidates.shape[0])):
            covered_groups = np.where(candidates[candidate_index,:] == 1)[0]
            unique_covered_groups = list(filter(lambda x: x not in present_groups, covered_groups))
            if len(unique_covered_groups) > 0:
                present_groups = np.append(present_groups, unique_covered_groups)
                result.append(candidate_index)
                
    return result


def first_genetic_algorithm(candidates, population_size, alpha, iter_num):
    
    
    def generate_population(population_size, groups):
        return np.random.randint(2, size=(population_size, groups))
    
    
    def get_score(groups,solution):
        included_members = np.where(solution == 1)[0]
        present_groups = np.empty(shape=(0,1))
        for index in included_members:
            covered_groups = np.where(candidates[index,:] == 1)[0]
            unique_covered_groups = list(filter(lambda x: x not in present_groups, covered_groups))
            present_groups = np.append(present_groups, unique_covered_groups)
        return len(present_groups) + len(solution) - len(included_members)
    
    
    def crossover(population):
        middle = int(len(population[0])/2)
        solution = [*population[-1][:middle], *population[0][middle:]]
        new_solutions = np.reshape(np.array(solution),(1,len(solution)))
        for index in range(len(population) - 1):
            solution = [*population[index][:middle],*population[index+1][middle:]]
            new_solutions = np.append(new_solutions, np.reshape(np.array(solution),(1,len(solution))), axis=0)
        return new_solutions
    
    
    def mutate(population, alpha):
        for solution in range(len(population)):
            for gen in range(len(population[solution,:])):
                if random.random() < alpha:
                    population[solution,gen] = abs(1-population[solution,gen])
        return population
    
    
    population = generate_population(population_size, candidates.shape[0])
    for i in range(iter_num):
        scores = list(map(lambda x: get_score(candidates.shape[1], x),population))
        zipped = list(zip(population.tolist(), scores))
        zipped.sort(reverse=True, key=lambda t: t[1])
        best_solutions = np.array(list(map(lambda x : x[0], zipped[0:int(len(zipped)/2)])))
        new_solutions = np.array(mutate(crossover(best_solutions), alpha))
        population = np.append(best_solutions, new_solutions, axis=0)

    scores = list(map(lambda x: get_score(candidates.shape[1], x),population))
    zipped = list(zip(population, scores))
    zipped.sort(reverse=True, key=lambda t: t[1])
    
    result = first_greedy_algorithm(candidates, np.where(zipped[0][0] == 1)[0].tolist())
    
    return result


def second_genetic_algorithm(candidates, population_size, alpha, iter_num):
    
    
    def generate_population(population_size, groups):
        return np.random.randint(2, size=(population_size, groups))
    
    
    def get_score(groups,solution):
        included_members = np.where(solution == 1)[0]
        present_groups = np.empty(shape=(0,1))
        
        for index in included_members:
            covered_groups = np.where(candidates[index,:] == 1)[0]
            unique_covered_groups = list(filter(lambda x: x not in present_groups, covered_groups))
            present_groups = np.append(present_groups, unique_covered_groups)
            
        return len(present_groups)**2 + (len(solution) - len(included_members))**2
    
    
    def crossover(zipped):
        population = np.array(list(map(lambda x : x[0], zipped)))
        scores = list(map(lambda x : x[1], zipped))
        probabilities = np.array([sum(scores[0:i+1])/sum(scores) for i in range(len(scores))])

        new_solutions = np.empty(shape=(1,len(population[0])))

        for _ in range(len(population)):

            rand_number = random.random()

            first_index = np.min(np.where(probabilities>rand_number))
            second_index = np.min(np.where(probabilities>(1-rand_number)))

            first_solution = population[first_index]
            second_solution = population[second_index]

            p = scores[first_index] / (scores[first_index] + scores[second_index])

            solution = []
            for gen in range(len(first_solution)):
                if random.random() <= p:
                    solution.append(first_solution[gen])
                else:
                    solution.append(second_solution[gen])
            new_solutions = np.append(new_solutions, np.reshape(np.array(solution),(1,len(solution))), axis=0)

        return new_solutions[1:]
    
    
    def mutate(population, alpha):
        for solution in range(len(population)):
            for gen in range(len(population[solution,:])):
                if random.random() < alpha:
                    population[solution,gen] = abs(1-population[solution,gen])
                    
                    
        return population
        
    
    
    population = generate_population(population_size, candidates.shape[0])
    for i in range(iter_num):
        scores = list(map(lambda x: get_score(candidates.shape[1], x),population))
        zipped = list(zip(population.tolist(), scores))
        zipped.sort(reverse=True, key=lambda t: t[1])
        best_solutions = np.array(list(map(lambda x : x[0], zipped[0:int(len(zipped)/2)])))
        new_solutions = np.array(mutate(crossover(zipped[0:int(len(zipped)/2)]), alpha))
        population = np.append(best_solutions, new_solutions, axis=0)

    scores = list(map(lambda x: get_score(candidates.shape[1], x),population))
    zipped = list(zip(population, scores))
    zipped.sort(reverse=True, key=lambda t: t[1])
    
    result = first_greedy_algorithm(candidates, np.where(zipped[0][0] == 1)[0].tolist())
    
    return result