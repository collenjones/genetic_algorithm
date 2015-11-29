from operator import add
from random import random, randint


def individual(length, min, max):
    """Create a member of the population."""
    return [randint(min, max) for x in xrange(length)]


def population(count, length, min, max):
    """Create a umber of individuals (i.e. a population).

    :count int: the number of individuals in the population
    :length int: the number of values per individuals
    :min int: the min possible value in an individual's list of values
    :max int: the max possible value in an individual's list of values
    """
    return [individual(length, min, max) for x in xrange(count)]


def fitness(individual, target):
    """Determine the fitness of an individual. Lower is better.

    :individual list: the individual to evaluage
    :target int: the sum of numbers that individuals are aiming for
    """
    sum = reduce(add, individual, 0)
    return abs(target - sum)


def grade(population, target):
    """Find average fitness for a population."""
    summed = reduce(add, (fitness(individual, target) for individual in population), 0)
    return summed / (len(population) * 1.0)


def evolve(population, target, retain=0.2, random_select=0.05, mutate=0.01):
    graded = [(fitness(individual, target), individual) for individual in population]
    graded = [fit_score[1] for fit_score in sorted(graded)]
    retain_length = int(len(graded)*retain)
    parents = graded[:retain_length]

    # randomly add other individuals to promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual)

    # mutate some individuals
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual) - 1)
            # this mutation is not ideal because it
            # restricts the range of possible values
            # but the function is unaware of the min/max
            # values used to create the individuals
            individual[pos_to_mutate] = randint(min(individual), max(individual))

    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(population) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length - 1)
        female = randint(0, parents_length - 1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = len(male) / 2
            child = male[:half] + female[:half]
            children.append(child)

    parents.extend(children)
    return parents


target = 371
population_count = 100
individual_length = 5
individual_min = 0
individual_max = 100
pop_instance = population(population_count, individual_length, individual_min, individual_max)
fitness_history = [grade(pop_instance, target),]

for i in xrange(100):
    population = evolve(pop_instance, target)
    fitness_history.append(grade(pop_instance, target))

for datum in fitness_history:
    print datum
