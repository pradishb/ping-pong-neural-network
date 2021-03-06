import numpy as np
import sys
import getopt
import matplotlib.pyplot as plt


class GeneticAlgorithm:
    def __init__(self, num_input, num_output, gui, save_file, fps):
        from one_player import Game

        self.gui = gui
        self.save_file = save_file
        self.my_game = Game(fps)

        self.num_input = num_input
        self.num_output = num_output

        self.sol_per_pop = 50
        self.num_parents = 20
        self.num_offspring = 20
        self.num_random_pop = 10
        self.num_generations = 1000

        self.num_weights = num_input * num_input + num_input * num_output

        self.pop_size = (self.sol_per_pop, self.num_weights)

        try:
            self.population = np.fromfile(
                self.save_file).reshape(self.pop_size)
            self.fitness_graph = np.fromfile(self.save_file + '_graph')
        except FileNotFoundError:
            self.population = np.random.uniform(
                low=-4.0, high=4.0, size=self.pop_size)
            self.fitness_graph = np.array([])

    def fitness(self):
        fitness_array = np.zeros(self.sol_per_pop)
        i = 0
        for weights in self.population:
            fitness_array[i] = self.my_game.find_fitness(weights, self.gui)
            i += 1
        return fitness_array

    def get_fitness_graph(self):
        return self.fitness_graph

    def print_population(self):
        print(self.population)

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
        # center crossover point
        # crossover_point = np.uint8(offspring_size[1]/2)
        # random crossover point
        crossover_point = np.random.randint(
            offspring_size[1] - 2, size=1)[0] + 1

        for k in range(offspring_size[0]):
            # Index of the first parent to mate.
            parent1_idx = np.random.randint(parents.shape[0], size=1)[0]
            # Index of the second parent to mate.
            parent2_idx = np.random.randint(parents.shape[0], size=1)[0]
            # The new offspring will have its first half of its genes taken from the first parent.
            offspring[k, 0:crossover_point] = parents[parent1_idx,
                                                      0: crossover_point]
            # The new offspring will have its second half of its genes taken from the second parent.
            offspring[k, crossover_point:] = parents[parent2_idx,
                                                     crossover_point:]
        return offspring

    def mutation(self, offspring_crossover):
        # Mutation changes a single random gene in each offspring randomly.
        for idx in range(offspring_crossover.shape[0]):
            # The random value to be added to the gene.
            random_value = np.random.uniform(-1.0, 1.0, 1)
            rand_gene = np.random.randint(
                offspring_crossover.shape[1], size=1)[0]
            offspring_crossover[idx, rand_gene] = offspring_crossover[idx,
                                                                      rand_gene] + random_value
        return offspring_crossover

    def train(self):
        # Training the AI using genetic algorithm

        for i in range(self.num_generations):
            # Calculating fitness
            fitness = self.fitness()
            max_fitness = int(np.max(fitness))
            print(fitness.astype(int), "Max Fitness: %i" % max_fitness)
            self.fitness_graph = np.concatenate(
                (self.fitness_graph, [max_fitness]))

            # Selecting best parents
            parents = self.select_mating_pool(fitness)

            # Crossover
            offspring_crossover = self.crossover(
                parents, (self.sol_per_pop - self.num_parents - self.num_random_pop, self.num_weights))

            # Adding some variations to the offsrping using mutation.
            offspring_mutation = self.mutation(offspring_crossover)

            # Some random new population
            random_population = np.random.uniform(
                low=-4.0, high=4.0, size=(self.num_random_pop, self.num_weights))

            # Creating the new population based on the parents and offspring.
            index1 = self.num_parents
            index2 = self.num_parents + self.num_offspring
            self.population[0:index1, :] = parents
            self.population[index1:index2, :] = offspring_mutation
            self.population[index2:, :] = random_population
        self.population.tofile(self.save_file)
        self.fitness_graph.tofile(self.save_file + '_graph')


def main(argv):
    gui = False
    data = ''
    fps = 15
    print_data = False
    print_graph = False
    try:
        opts, args = getopt.getopt(
            argv, "hpgd:f:", ["graph", "print", "gui", "data=", "fps="])
    except getopt.GetoptError:
        print('error in options. try -h')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Not set')
            sys.exit()
        elif opt in ("-p", "--print"):
            print_data = True
        elif opt in ("-gr", "--graph"):
            print_graph = True
        elif opt in ("-g", "--gui"):
            gui = True
        elif opt in ("-d", "--data"):
            data = arg
        elif opt in ("-f", "--fps"):
            fps = arg
    return [gui, data, fps, print_data, print_graph]


if __name__ == '__main__':
    args = main(sys.argv[1:])
    ga = GeneticAlgorithm(3, 2, args[0], args[1], args[2])
    if args[3]:
        ga.print_population()
    elif args[4]:
        plt.plot(ga.get_fitness_graph())
        plt.show()
    else:
        ga.train()
        plt.plot(ga.get_fitness_graph())
        plt.show()
