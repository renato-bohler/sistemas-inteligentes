from Genetic import Genetic
import Busca_Largura
from RobotControl import RobotControl

initial_position = (9, 9, 'W')
final_position = (8, 2, 'S')
maximum_generations = 20

genetic = Genetic(initial_position, final_position, population_size=10, mutation_probability=0.01, map_size=10, with_elitism=True)

for i in range(maximum_generations):
	next_generation = genetic.generateNextGeneration()
	# print(genetic.best_score)
	# print(genetic.best_chromosome)

# print(genetic.best_chromosome)

first_path_segment = Busca_Largura.search(initial_position, genetic.best_chromosome)
final_path_segment = Busca_Largura.search(genetic.best_chromosome, final_position)

full_path = first_path_segment + final_path_segment

print(full_path)
RobotControl.execute_commands(full_path)

