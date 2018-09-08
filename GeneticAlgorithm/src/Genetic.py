import random
import numpy as np

class Genetic():

	def __init__(self, population_size=10, chromosome_size=10, mutation_probability=0.02, with_elitism=False):
		self.mutation_probability = mutation_probability
		self.population_size = population_size
		self.with_elitism = with_elitism
		self.chromosome_size = chromosome_size
		self.current_generation = self._generateRandomPopulation()

	def _mutation(self, chromosome):
		for index, gene in enumerate(chromosome):
			if random.random() < self.mutation_probability:
				chromosome[index] = 0 if gene == 1 else 1

	def _crossover(self, first_chromosome, second_chromosome):
		crossover_point = np.random.randint(1, len(first_chromosome))
		new_first_chromosome = first_chromosome[0:crossover_point] + second_chromosome[crossover_point:len(first_chromosome)]
		new_second_chromosome = second_chromosome[0:crossover_point] + first_chromosome[crossover_point:len(first_chromosome)]
		return new_first_chromosome, new_second_chromosome

	def _evaluateChromossome(self, chromosome):
		return 0

	def nextGeneration(self):
		generation = []

		for chromosome in self.current_generation:
			self._mutation(chromosome)

		return generation

	def evaluatePopulation(self):
		return 0

	def _generateRandomPopulation(self):
		population = []
		for chromosome in range(self.population_size):
			population.append(self._randomChromosome())

		return population

	def _randomChromosome(self):
		chromosome = []
		for gene in range(self.chromosome_size):
			chromosome.append(random.randint(0,1))
		return chromosome
