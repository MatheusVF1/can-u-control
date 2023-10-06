import numpy as np

from lands import *

def maximum(land, level):
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
    bestDist = np.inf
    bestI = 0        
    uMax = maximum(land, level)
    for i in range(-uMax, uMax + 1):
        valueUI = i / uMax
        minimumDistance = np.inf
        distance = np.inf
        x1 = x
        y1 = y
        u = valueUI
        for k in range(quant):
            for q in range(len(BonusX)):
                f = 1 if q == 0 else 2
                distance = f*((x1 - BonusX[q])*(x1 - BonusX[q]) + (y1 - BonusY[q])*(y1 - BonusY[q]))
                if (distance < minimumDistance):
                    minimumDistance = distance
            l12 = define_maps_equations(land, level, x1, y1, u)
            x1 += l12[0]*dt
            y1 += l12[1]*dt
            if(minimumDistance < bestDist):
                bestDist = minimumDistance
                bestI = valueUI
        for j in range(-uMax, uMax + 1):
            valorUJ = j / uMax
            x11 = x1
            y11 = y1
            u = valorUJ
            for k in range(quant):
                for q in range(len(BonusX)):
                    f = 1 if q == 0 else 2
                    distance = f*((x11 - BonusX[q])*(x11 - BonusX[q]) + (y11 - BonusY[q])*(y11 - BonusY[q]))
                    if (distance < minimumDistance): 
                        minimumDistance = distance
                l12 = define_maps_equations(land, level, x11, y11, u)
                x11 += l12[0]*dt
                y11 += l12[1]*dt

                if(minimumDistance < bestDist):
                    bestDist = minimumDistance
                    bestI = valueUI
    return bestI
