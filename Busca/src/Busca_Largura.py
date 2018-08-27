# Autores: Davi Boberg e Renato Böhler

from Node import Node
from RobotControl import RobotControl

# Representação do estado
# (x,     y,     d        )
# ([0 9], [0 9], {W,A,S,D})
estadoInicial = (9,9,'W')
estadoFinal = (8,2,'S')

# Funções

# Recebe dois estados adjacentes e determina a ação necessária para realizar a transição
def determinar_acao(origem, destino):        
        delta_x = destino[0] - origem[0]
        delta_y = destino[1] - origem[1]
        d_origem = origem[2]
        d_destino = destino[2]

        if (delta_y == -1 and d_origem == 'W' and d_destino == 'W') or (delta_x == -1 and d_origem == 'A' and d_destino == 'A') or (delta_y == -1 and d_origem == 'S' and d_destino == 'S') or (delta_x == 1 and d_origem == 'D' and d_destino == 'D'):
                # Mover para frente
                return 'straight'
        elif (d_origem == 'W' and d_destino == 'A') or (d_origem == 'A' and d_destino == 'S') or (d_origem == 'S' and d_destino == 'D') or (d_origem == 'D' and d_destino == 'W'):
                # Rotacionar para esquerda
                return 'left'
        elif (d_origem == 'W' and d_destino == 'D') or (d_origem == 'D' and d_destino == 'S') or (d_origem == 'S' and d_destino == 'A') or (d_origem == 'A' and d_destino == 'W'):
                # Rotacionar para direita
                return 'right'

        raise Exception('Os estados {origem} e {destino} não são adjacentes'.format(origem=origem, destino=destino))

# Recebe o nó destino e retorna a sequência de estados adjacentes da raiz até ele
def determinar_caminho(destino, printCaminho = True):
        caminho = [destino.data]

        noAtual = destino
        while noAtual.parent != None:
                caminho.insert(0, noAtual.parent.data)
                noAtual = noAtual.parent
        
        if printCaminho == True:
                print("Caminho gerado: {caminho}".format(caminho=caminho))
                print()
        return caminho

def imprimir_caminho(caminho):
	linha = 0
	while linha <= 9:
		coluna = 0
		while coluna <= 9:
			if [True for node in caminho if linha == node[1] and coluna == node[0]]:
				print('o', end='')
			elif coluna == 8 and linha == 28:
				print('g', end='')
			elif coluna > 3 and linha == 5:
				print('x', end='')
			else:
				print('-', end='')

			coluna += 1
		linha += 1
		print()
	print()

# Recebe o nó destino e retorna a sequência de ações para alcançá-lo
def gerar_planejamento(destino):
        acoes = []
        caminho = determinar_caminho(destino, False)
        
        if len(caminho) < 2:
                return acoes

        origem = caminho.pop(0)
        while caminho:
                destino = caminho.pop(0)
                acoes.append(determinar_acao(origem, destino))
                origem = destino

        print("*** Tamanho do caminho encontrado: {tamanho} passos".format(tamanho=len(acoes)))
        print("Planejamento gerado: {planejamento}".format(planejamento=acoes))
        print()
        return acoes

# Recebe um estado e retorna uma lista com todas as transições possíveis para ele
def transicoes_possiveis(estado):
        movimentos_possiveis = ['straight', 'left', 'right']
        
        x = estado[0]
        y = estado[1]
        d = estado[2]

        # Limites do mapa
        if (y == 0 and d == 'W') or (x == 0 and d == 'A') or (y == 9 and d == 'S') or (x == 9 and d == 'D'):
                movimentos_possiveis.remove('straight')

        # Obstruções do mapa

        # Parte inferior da obstrução
        if x >= 4 and y == 6 and d == 'W':
                movimentos_possiveis.remove('straight')

        # Parte lateral da obstrução
        if x == 3 and y == 5 and d == 'D':
                movimentos_possiveis.remove('straight')

        # Parte superior da obstrução
        if x >= 4 and y == 4 and d == 'S':
                movimentos_possiveis.remove('straight')

        return estados_possiveis(estado, movimentos_possiveis)

# Recebe um estado e uma lista de movimentos possíveis e retorna os estados possíveis
def estados_possiveis(estado, movimentos_possiveis):        
        estados = set()

        x = estado[0]
        y = estado[1]
        d = estado[2]

        # Pode andar para frente
        if 'straight' in movimentos_possiveis:
                novo_x = x
                novo_y = y

                if d == 'W':
                        novo_y = y-1
                elif d == 'A':
                        novo_x = x-1
                elif d == 'S':
                        novo_y = y+1
                elif d == 'D':
                        novo_x = x+1

                estados.add((novo_x, novo_y, d))

        # Pode rotacionar para esquerda
        if 'left' in movimentos_possiveis:
                nova_direcao = d
                
                if d == 'W':
                        nova_direcao = 'A'
                elif d == 'A':
                        nova_direcao = 'S'
                elif d == 'S':
                        nova_direcao = 'D'
                elif d == 'D':
                        nova_direcao = 'W'

                estados.add((x,y,nova_direcao))

        # Pode rotacionar para direita
        if 'right' in movimentos_possiveis:
                nova_direcao = d

                if d == 'W':
                        nova_direcao = 'D'
                elif d == 'A':
                        nova_direcao = 'W'
                elif d == 'S':
                        nova_direcao = 'A'
                elif d == 'D':
                        nova_direcao = 'S'

                estados.add((x,y,nova_direcao))
                
        return estados

# Realiza a busca em largura, retornando uma sequência de passos para atingir o destino a partir da origem
def busca_largura(origem, destino):
        # Raíz da árvore
        noAtual = Node(origem, None)
        pendentes = [noAtual]
        visitados = set()

        while pendentes:
                noAtual = pendentes.pop(0)
                if noAtual.data not in visitados:
                        transicoes = transicoes_possiveis(noAtual.data)
                        for transicao in transicoes:
                                transicaoNo = Node(transicao, noAtual)
                                
                                if transicao == destino:
                                        visitados.add(noAtual.data)
                                        print("*** {avaliados} estados avaliados".format(avaliados=len(visitados)))
                                        imprimir_caminho(determinar_caminho(transicaoNo))
                                        return gerar_planejamento(transicaoNo)
                                
                                pendentes.append(transicaoNo)

                        visitados.add(noAtual.data)

        raise Exception('O estado {destino} não é alcançável a partir de {origem}'.format(origem=origem, destino=destino))

# Executa as ações do planejamento dado
def executar_planejamento(planejamento):
        robot_control = RobotControl()

        while planejamento and robot_control.simulator.isConnected():
                acao = planejamento.pop(0)

                if acao == 'straight':
                        print("Seguindo em frente...")
                elif acao == 'left':
                        print("Virando para a esquerda...")
                elif acao == 'right':
                        print("Virando para a direita...")

                robot_control.run(acao)
        
        print("Planejamento executado")
        print()
        robot_control.simulator.close()


def execute():
    print("Origem: {origem}".format(origem=estadoInicial))
    print("Destino: {destino}".format(destino=estadoFinal))
    print()
    planejamento = busca_largura(estadoInicial, estadoFinal)
    executar_planejamento(planejamento)

if __name__ == '__main__':
    execute()