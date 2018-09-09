from Genetic import Genetic

initial_position = (9, 9, 'W')
final_position = (8, 2, 'S')

genetic = Genetic(initial_position, final_position, population_size=10, mutation_probability=0.01, map_size=10, with_elitism=True)

for i in range(100):
	next_generation = genetic.generateNextGeneration()
	print(genetic.best_score)

print(genetic.best_chromosome)
