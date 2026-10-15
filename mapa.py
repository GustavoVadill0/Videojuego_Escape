import random
from collections import deque
from config import *

# Tu mapa con 4 llaves extra agregadas en la Fila 5 (el pasillo largo)
MAPA_STR = [
    "511111111111111111115",
    "500005000005000050005",
    "503002003002000050305",
    "500005000005000050005",
    "512111110111112111015",
    "500300000300000300005", # <- Fila 5: Llaves añadidas aquí
    "500001112111110111015",
    "500301000001000500005",
    "511011000001030200005",
    "500002000002000500005",
    "500001111111111111215",
    "510111000001000000005",
    "500001003001000011015",
    "500302000001003010005",
    "511011112111112110005",
    "521110000000000110115",
    "510000100000111111115",
    "503001110111000020005",
    "500000000000003010005",
    "500001111111000010005",
    "511111111111111111115"
]

MAPA_ORIGINAL = [[int(char) for char in fila] for fila in MAPA_STR]

class GestorNivel:
    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        self.matriz = [fila[:] for fila in MAPA_ORIGINAL]
        self.llaves_recolectadas = 0
        
        # 2. Escaneamos la matriz buscando todas las casillas vacías (0)
        casillas_libres = []
        for y in range(FILAS):
            for x in range(COLUMNAS):
                # Validamos que sea suelo vacío. 
                # Además evitamos que la salida aparezca justo donde naces (1, 5) 
                # o donde nace el monstruo (10, 5).
                if self.matriz[y][x] == 0 and (x, y) != (1, 5) and (x, y) != (10, 5):
                    casillas_libres.append((x, y))
        
        # 3. Elegimos una casilla libre al azar y le ponemos el 4 (Salida Morada)
        if casillas_libres:
            sx, sy = random.choice(casillas_libres)
            self.matriz[sy][sx] = 4

    def bfs_pathfinding(self, inicio_x, inicio_y, objetivo_x, objetivo_y):
        visitados = set()
        visitados.add((inicio_x, inicio_y))
        cola = deque([(inicio_x, inicio_y, [])])
        direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        while cola:
            ax, ay, camino = cola.popleft()
            if ax == objetivo_x and ay == objetivo_y:
                return camino[0] if camino else (inicio_x, inicio_y)
                
            for dx, dy in direcciones:
                nx, ny = ax + dx, ay + dy
                if 0 <= nx < COLUMNAS and 0 <= ny < FILAS:
                    if self.matriz[ny][nx] in [0, 3, 4] and (nx, ny) not in visitados:
                        visitados.add((nx, ny))
                        cola.append((nx, ny, camino + [(nx, ny)]))
        return (inicio_x, inicio_y)