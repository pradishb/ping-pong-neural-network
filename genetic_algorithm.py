import numpy as np
from one_player import Game


def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


class GeneticAlgorithm:
    def __init__(self, num_input, num_output):
        self.my_game = Game()

        self.num_input = num_input
        self.num_output = num_output

        self.sol_per_pop = 50
        self.num_parents = 2

        self.num_weights = num_input * num_input + num_input * num_output

        self.pop_size = (self.sol_per_pop, self.num_weights)

        self.population = np.random.uniform(
            low=-4.0, high=4.0, size=self.pop_size)

        self.num_generations = 100

    def fitness(self):
        fitness_array = np.zeros(self.sol_per_pop)
        i = 0
        for weights in self.population:
            fitness_array[i] = self.my_game.find_fitness_gui(weights)
            i += 1

        return fitness_array

    def select_mating_pool(self, fitness):
        # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
        parents = np.empty((self.num_parents, self.population.shape[1]))
        for parent_num in range(self.num_parents):
            max_fitness_idx = np.where(fitness == np.max(fitness))
            max_fitness_idx = max_fitness_idx[0][0]
            parents[parent_num, :] = self.population[max_fitness_idx, :]
            fitness[max_fitness_idx] = -99999999999
        return parents

    def crossover(self, parents, offspring_size):
        offspring = np.empty(offspring_size)
        # The point at which crossover takes place between two parents. Usually it is at the center.
        crossover_point = np.uint8(offspring_size[1]/2)

        for k in range(offspring_size[0]):
            # Index of the first parent to mate.
            parent1_idx = k % parents.shape[0]
            # Index of the second parent to mate.
            parent2_idx = (k+1) % parents.shape[0]
            # The new offspring will have its first half of its genes taken from the first parent.
            offspring[k, 0:crossover_point] = parents[parent1_idx,
                                                      0:crossover_point]
            # The new offspring will have its second half of its genes taken from the second parent.
            offspring[k, crossover_point:] = parents[parent2_idx,
                                                     crossover_point:]
        return offspring

    def mutation(self, offspring_crossover):
        # Mutation changes a single gene in each offspring randomly.
        for idx in range(offspring_crossover.shape[0]):
            # The random value to be added to the gene.
            random_value = np.random.uniform(-1.0, 1.0, 1)
            offspring_crossover[idx,
                                4] = offspring_crossover[idx, 4] + random_value
        return offspring_crossover

    def train(self):
        # Generating next generation using crossover.

        for i in range(self.num_generations):

            fitness = self.fitness()
            print(fitness.astype(int), "Max Fitness: %i" %
                  int(np.max(fitness)))

            parents = self.select_mating_pool(fitness)

            offspring_crossover = self.crossover(
                parents, (self.sol_per_pop - self.num_parents, self.num_weights))

            # Adding some variations to the offsrping using mutation.
            offspring_mutation = self.mutation(offspring_crossover)

            # Creating the new population based on the parents and offspring.
            self.population[0:parents.shape[0], :] = parents
            self.population[parents.shape[0]:, :] = offspring_mutation


if __name__ == '__main__':
    ga = GeneticAlgorithm(12, 2)
    ga.train()
