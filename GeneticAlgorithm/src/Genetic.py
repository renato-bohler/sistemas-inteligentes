import random
import numpy as np
import Penalty

class Genetic():

	__directions = ['W', 'S', 'A', 'D']
	__obstacles_position = [(4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5)]

	def __init__(self, initial_position=(0,0), final_position=(9,9), population_size=10, mutation_probability=0.02, map_size=10, with_elitism=False):
		self.mutation_probability = mutation_probability
		self.population_size = population_size
		self.with_elitism = with_elitism
		self.map_size = map_size
		self.initial_position = initial_position
		self.final_position = final_position
		self.population = self.__generateRandomPopulation()

	def __mutation(self, chromosome):
		binary = f'{chromosome[0]:04b}' + f'{chromosome[1]:04b}'

		binaries = ''
		for index, gene in enumerate(binary):
			if np.random.random_sample() < self.mutation_probability:
				binaries += '0' if gene == '1' else '1'
			else:
				binaries += gene

		direction = chromosome[2]
		if np.random.random_sample() < self.mutation_probability:
			direction = np.random.choice(self.__directions)

		x = binaries[0:4]
		y = binaries[4:len(binaries)]
		x = int(x, 2)
		y = int(y, 2)
		return (x,y, direction)

	def __crossover(self, first_chromosome, second_chromosome):
		number_of_crossover = np.random.randint(1, 3)
		if number_of_crossover == 1:
			crossover_point = np.random.randint(1, len(first_chromosome))
		else:
			if np.random.choice(2) is 0:
				return (first_chromosome[0], second_chromosome[1], first_chromosome[2])
			else:
				return (second_chromosome[0], first_chromosome[1], second_chromosome[2])

		if np.random.choice(2) is 0:
			return first_chromosome[0:crossover_point] + second_chromosome[crossover_point:len(first_chromosome)]
		else:
			return second_chromosome[0:crossover_point] + first_chromosome[crossover_point:len(first_chromosome)]


	def generateNextGeneration(self):
		scores = self.__evaluatePopulation()
		new_generation = self.__selection(scores)

		for index, chromosome in enumerate(new_generation):
			mutated = self.__mutation(chromosome)
			new_generation[index] = mutated

		self.population = new_generation
		return self.population

	def __selection(self, population_score):
		new_generation = []

		population_to_generate = self.population_size
		if self.with_elitism:
			new_generation.append(self.population[population_score.index(min(population_score))])
			population_to_generate -= 1

		for i in range(population_to_generate):
			first_selected_index = self.__selectChromosome(population_score)
			second_selected_index = self.__selectChromosome(population_score)
			first_chromosome = self.population[first_selected_index]
			second_chromosome = self.population[second_selected_index]

			new_generation.append(self.__crossover(first_chromosome, second_chromosome))

		return new_generation

	def __selectChromosome(self, population_score):
		choice_chromosomes = np.random.choice(self.population_size, 2, replace=False)

		first_index = choice_chromosomes[0]
		second_index = choice_chromosomes[1]

		first_score = population_score[first_index]
		second_score = population_score[second_index]

		if first_score >= second_score:
			return first_index
		else:
			return second_index

	def __evaluatePopulation(self, population = None):
		population = population if population is not None else self.population
		chromosomes_score = []
		for chromosome in population:
			penalty = self.__penalty(chromosome)
			score = self.__score(chromosome)
			chromosomes_score.append(penalty + score)
		self.best_score = min(chromosomes_score)
		self.best_chromosome = population[chromosomes_score.index(self.best_score)]
		return chromosomes_score

	def __penalty(self, chromosome) -> float:
		penalty = Penalty.penalty(self.initial_position, chromosome)
		penalty += Penalty.penalty(chromosome, self.final_position)
		return penalty

	def __score(self, chromosome) -> float:
		score = self.__euclidianDistance(self.initial_position, chromosome)
		score += self.__euclidianDistance(chromosome, self.final_position)
		return score

	def __euclidianDistance(self, origin, destiny):
		origin = np.array([origin[0], origin[1]])
		destiny = np.array([destiny[0], destiny[1]])
		return np.linalg.norm(origin - destiny)

	def __generateRandomPopulation(self):
		population = []
		for chromosome in range(self.population_size):
			population.append(self.__randomChromosome())

		self.__evaluatePopulation(population)
		return population

	def __randomChromosome(self):
		while True:
			first_choice = np.random.choice(self.map_size)
			second_choice = np.random.choice(self.map_size)

			if (first_choice, second_choice) not in self.__obstacles_position:
				break

		direction = np.random.choice(self.__directions)
		chromosome = (first_choice, second_choice, direction)
		return chromosome
