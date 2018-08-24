# Funções

# Recebe um estado e retorna uma lista com todas as transições possíveis para ele
def transicoes_possiveis(estado):
        movimentos_possiveis = set(['8', '4', '6'])
        
        x = estado[0]
        y = estado[1]
        d = estado[2]

        # Limites do mapa
        if (y == 0 and d == 'W') or (x == 0 and d == 'A') or (y == 9 and d == 'S') or (x == 9 and d == 'D'):
                movimentos_possiveis.remove('8')

        # Obstruções do mapa

        # Parte inferior da obstrução
        if x >= 4 and y == 6 and d == 'W':
                movimentos_possiveis.remove('8')

        # Parte lateral da obstrução
        if x == 3 and y == 5 and d == 'D':
                movimentos_possiveis.remove('8')

        # Parte superior da obstrução
        if x >= 4 and y == 4 and d == 'S':
                movimentos_possiveis.remove('8')

        return estados_possiveis(estado, movimentos_possiveis)

# Recebe um estado e uma lista de movimentos possíveis e retorna os estados possíveis
def estados_possiveis(estado, movimentos_possiveis):        
        estados = set()

        x = estado[0]
        y = estado[1]
        d = estado[2]

        # Pode andar para frente
        if '8' in movimentos_possiveis:
                novo_x = x;
                novo_y = y;

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
        if '4' in movimentos_possiveis:
                nova_direcao = d;
                
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
        if '6' in movimentos_possiveis:
                nova_direcao = d;

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

def construir_grafo(estadoInicial):
        grafo = dict()
        estadoAtual = estadoInicial
        pendentes = [estadoInicial]
        visitados = set()

        while pendentes:
                if estadoAtual not in visitados:
                        visitados.add(estadoAtual)
                        transicoes = transicoes_possiveis(estadoAtual)
                        grafo[estadoAtual] = transicoes
                        pendentes.extend(list(transicoes))
                estadoAtual = pendentes.pop()
        return grafo
        
# Representação do estado
# (x,     y,     d        )
# ([0 9], [0 9], {W,A,S,D})
estadoInicial = (9,9,'W')
estadoFinal = (8,2,'S')

# Caminhos que já foram visitados
visitados = set(estadoInicial)
# Caminho planejado
caminho = []

print(construir_grafo(estadoInicial))
