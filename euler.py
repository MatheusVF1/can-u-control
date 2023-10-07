import numpy as np

from lands import *

def maximum(land, level):
    # Calcula o valor máximo de `u` para a land e level dados.
    uMax = 10
    if land == 1:
        if level == 3 or level == 4:
            uMax = 8
    if land == 2:
        if level == 2 or level == 4:
            uMax = 10
        elif level == 3:
            uMax = 9
    if land == 3:
        if level == 2 or level == 4:
            uMax = 8
    if land == 4:
        if level == 1 or level == 3:
            uMax = 8
        elif level == 4:
            uMax = 10
    return uMax



def calculate_distances(x, y, land, level, quant, dt, BonusX, BonusY, SkullsX, SkullsY):
    """
    Calcula a melhor direção que o jogador deve tomar para minimizar a distância até todos os bônus.

    Args:
        x: A coordenada x do jogador.
        y: A coordenada y do jogador.
        land: Qual a ilha atual.
        level: Qual o nivel atual.
        dt: O passo de tempo.
        BonusX: Uma lista de coordenadas x dos bônus.
        BonusY: Uma lista de coordenadas y dos bônus.
        SkullsX: Uma lista de coordenadas x dos crânios.
        SkullsY: Uma lista de coordenadas y dos crânios.

    Returns:
        O melhor valor de `u`.
    """  
    
    # Inicializa a melhor distância como infinito
    bestDist = np.inf

    # Inicializa o melhor valor de `u` como zero.
    bestI = 0 

    # Calcula o máximo valor de `u` para o terreno e o nível dados.
    uMax = maximum(land, level)

    # Para cada valor de `u` de `-uMax` a `uMax`, calcula a distância até todos os bônus simulando o movimento do jogador por `quant` passos de tempo.

    for i in range(-uMax, uMax + 1):
         # Calcula o valor de `u` atual dividido por `uMax`.
        valueUI = i / uMax

        # Inicializa a distância mínima até todos os bônus para o valor atual de `u` como infinito.
        minimumDistance = np.inf
        distance = np.inf

        # posições de x e y
        x1 = x
        y1 = y
        u = valueUI
        for k in range(quant):
            
            # Para cada passo de tempo, a função calcula a distância até o bônus mais próximo. Se a distância for menor que minimumDistance, minimumDistance é atualizada.
            for q in range(len(BonusX)):
                f = 1 if q == 0 else 2
                distance = f*((x1 - BonusX[q])*(x1 - BonusX[q]) + (y1 - BonusY[q])*(y1 - BonusY[q]))
                if (distance < minimumDistance):
                    minimumDistance = distance
            l12 = define_maps_equations(land, level, x1, y1, u)
            x1 += l12[0]*dt
            y1 += l12[1]*dt
            # Se minimumDistance for menor que bestDist, bestDist é atualizada com o novo valor.
            if(minimumDistance < bestDist):
                bestDist = minimumDistance
                bestI = valueUI
        for j in range(-uMax, uMax + 1):
            valorUJ = j / uMax
            x11 = x1
            y11 = y1
            u = valorUJ
            # Simula o movimento do jogador por `quant` passos de tempo.
            for k in range(quant):
                # Calcula a distância até o bônus mais próximo.
                for q in range(len(BonusX)):
                    f = 1 if q == 0 else 2
                    distance = f*((x11 - BonusX[q])*(x11 - BonusX[q]) + (y11 - BonusY[q])*(y11 - BonusY[q]))
                    if (distance < minimumDistance): 
                        minimumDistance = distance
                 # Atualiza a posição do jogador.
                l12 = define_maps_equations(land, level, x11, y11, u)
                x11 += l12[0]*dt
                y11 += l12[1]*dt

                # Se a distância mínima até todos os bônus for menor que a melhor distância, atualiza a melhor distância e o melhor valor de `u`.
                if(minimumDistance < bestDist):
                    bestDist = minimumDistance
                    bestI = valueUI
    return bestI
