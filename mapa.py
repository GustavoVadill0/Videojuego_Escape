import random
from collections import deque
from config import *

MAPA_STR = [
    "511111111111111111115",
    "500005000005000050005",
    "503002003002000050305",
    "500005000005000050005",
    "512111110111112111015",
    "500300000300000300005",
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

class Nivel:
    def __init__(self):
        self.llaves_recolectadas = 0
        self.matriz = []
        self.cargar_mapa()

    def cargar_mapa(self):
        # 1. Convertimos el mapa de texto a matriz numérica
        self.matriz = [[int(char) for char in fila] for fila in MAPA_STR]
        
        # 2. Escaneamos las casillas vacías (0) para colocar la salida (4)
        casillas_libres = []
        filas = len(self.matriz)
        columnas = len(self.matriz[0])

        for y in range(filas):
            for x in range(columnas):
                # Evitamos spawn del jugador (1, 5) y del monstruo (10, 5)
                if self.matriz[y][x] == 0 and (x, y) != (1, 5) and (x, y) != (10, 5):
                    casillas_libres.append((x, y))

        # 3. Colocamos la salida '4' en una posición aleatoria válida
        if casillas_libres:
            sx, sy = random.choice(casillas_libres)
            self.matriz[sy][sx] = 4

    def reiniciar(self):
        self.llaves_recolectadas = 0
        self.cargar_mapa()

    def bfs_pathfinding(self, inicio_x, inicio_y, destino_x, destino_y):
        if inicio_x == destino_x and inicio_y == destino_y:
            return inicio_x, inicio_y

        cola = deque([(inicio_x, inicio_y, [])])
        visitados = {(inicio_x, inicio_y)}

        while cola:
            x, y, camino = cola.popleft()

            if x == destino_x and y == destino_y:
                if camino:
                    return camino[0]
                return inicio_x, inicio_y

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy

                if 0 <= ny < len(self.matriz) and 0 <= nx < len(self.matriz[0]):
                    if (nx, ny) not in visitados:
                        casilla = self.matriz[ny][nx]
                        # El monstruo no atraviesa muros (1, 5) ni puertas cerradas (2)
                        if casilla not in (1, 5, 2):
                            visitados.add((nx, ny))
                            cola.append((nx, ny, camino + [(nx, ny)]))

        return inicio_x, inicio_y