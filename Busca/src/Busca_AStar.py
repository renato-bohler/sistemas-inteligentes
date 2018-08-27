from Node import Node
from RobotControl import RobotControl
import Busca

# Representação do estado
# (x,     y,     d        )
# ([0 9], [0 9], {W,A,S,D})
estadoInicial = (9, 9, 'W')
estadoFinal = (8, 2, 'S')

def getKey(item):
	return item[1]

def getShortest(list_of_nodes):
	list_of_nodes.sort(key=getKey)
	node = list_of_nodes.pop(0)
	return node[0]

def heuristic(a, b):
	(x1, y1, dir) = a
	(x2, y2, dir) = b
	return abs(x1 - x2) + abs(y1 - y2)

def A_Star_search(start, goal):
	origin = Node(start, None)
	openNodes = [[origin, 0]]
	cost_so_far  = {}
	cost_so_far[repr(start)] = 0

	while openNodes:
		current = getShortest(openNodes)

		if current.data == goal:
			planning = Busca.gerar_planejamento(current)
			Busca.printPlanning(Busca.determinar_caminho(current))
			return planning

		neighbors_data = Busca.transicoes_possiveis(current.data)
		for neighbor_data in neighbors_data:

			new_cost = cost_so_far[repr(current.data)] + 1

			if repr(neighbor_data) not in cost_so_far or new_cost < cost_so_far[repr(neighbor_data)]:
				cost_so_far[repr(neighbor_data)] = new_cost
				heuristic_cost = cost_so_far[repr(current.data)] + heuristic(goal, neighbor_data)
				openNodes.append([Node(neighbor_data, current),  heuristic_cost])

	raise Exception('O estado {destino} não é alcançável a partir de {origem}'.format(origem=start, destino=goal))

#def execute():
print("Origem: {origem}".format(origem=estadoInicial))
print("Destino: {destino}".format(destino=estadoFinal))
print("")
planejamento = A_Star_search(estadoInicial, estadoFinal)
Busca.executar_planejamento(planejamento)