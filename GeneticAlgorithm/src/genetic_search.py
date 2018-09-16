# Autores: Davi Boberg e Renato Böhler
from Genetic import Genetic
import Busca_Largura
from RobotControl import RobotControl

initial_position = (9, 9, 'W')
final_position = (8, 2, 'S')
maximum_generations = 50

genetic = Genetic(initial_position, final_position, population_size=20, mutation_probability=0.01, map_size=10, with_elitism=True)

for i in range(maximum_generations):
	next_generation = genetic.generateNextGeneration()
	# print(genetic.best_score)
	# print(genetic.best_chromosome)

print("Melhor cromossomo: {best_chromosome}".format(best_chromosome=genetic.best_chromosome))
print("Avaliação: {best_score}".format(best_score=genetic.best_score))
print()

print("Primeira parte do caminho:")
first_path_segment = Busca_Largura.search(initial_position, genetic.best_chromosome)

print("Parte final do caminho:")
final_path_segment = Busca_Largura.search(genetic.best_chromosome, final_position)

full_path = first_path_segment + final_path_segment

print("Caminho encontrado ({size} passos):".format(size=len(full_path)))
print(full_path)

RobotControl.execute_commands(full_path)

