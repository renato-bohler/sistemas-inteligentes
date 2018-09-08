# Autores: Davi Boberg e Renato Böhler

# Penalidade aplicada
penaltyAmount = 1000

# "Granularidade" de cada quadrado da cena
divisonsPerUnit = 100

# Limites da parede da cena
YL1 = 4.5 * divisonsPerUnit
YL2 = 5.5 * divisonsPerUnit
XL3 = 3.5 * divisonsPerUnit

# Cálculo da penalidade ao sair de origem ir a destino
def penalty(origem, destino):
    c_origem = _convertStateToCoordinates(origem)
    c_destino = _convertStateToCoordinates(destino)

    x = c_origem[0]
    y = c_origem[1]

    x0 = c_destino[0]
    y0 = c_destino[1]
    
    # Mesmo ponto
    if (x == x0 and y == y0):
        return 0
    
    # Coeficiente angular infinito
    if (x == x0):
        if (x >= XL3):
            return penaltyAmount
        return 0

    # Coeficiente angular nulo
    if (y == y0):
        if (YL1 <= y and y <= YL2):
            return penaltyAmount
        return 0

    # Demais casos
    # Coeficiente angular
    a = (y - y0) / (x - x0)

    # Coeficiente linear
    b = y - a * x

    # Limite 1
    XL1 = (YL1 - b) / a    
    if XL1 >= XL3:
        return penaltyAmount

    # Limite 2
    XL2 = (YL2 - b) / a
    if XL2 >= XL3:
        return penaltyAmount

    # Limite 3
    YL3 = a * XL3 + b
    if YL1 <= YL3 and YL3 <= YL2:
        return penaltyAmount
    
    return 0

# Converte um estado (x, y, D) para suas respectivas coordenadas
def _convertStateToCoordinates(state):
    return (state[0] * divisonsPerUnit,state[1] * divisonsPerUnit)