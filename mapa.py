import random
from collections import deque

# ---------------------------------------------------------------------------
# NIVELES
#   0 = suelo     1 = muro horizontal   5 = muro vertical
#   2 = puerta    3 = llave
#   (la salida "4" y los poderes "6, 7, 8" se colocan al azar al cargar)
#
# Tamanos: Nivel 1 = 11x11, 2 = 15x15, 3 = 17x17, 4 = 21x21 (el original),
#          5 = 27x27
# ---------------------------------------------------------------------------
NIVELES = [
    {
        "nombre": "Nivel 1",
        "jugador": (1, 1),
        "monstruo": (1, 9),
        # Multiplicadores de dificultad (se combinan con Facil/Normal/Dificil)
        "factor_velocidad_monstruo": 1.5,   # >1 = monstruo mas lento
        "factor_luz": 1.4,                  # >1 = mas vision
        "mapa": [
            "51111111115",
            "50000000005",
            "50505050505",
            "50000000505",
            "50111211115",
            "50502053035",
            "50111110505",
            "50000000505",
            "50111111105",
            "50030000005",
            "51111111115"
        ]
    },
    {
        "nombre": "Nivel 2",
        "jugador": (1, 13),
        "monstruo": (7, 5),
        # Multiplicadores de dificultad (se combinan con Facil/Normal/Dificil)
        "factor_velocidad_monstruo": 1.3,   # >1 = monstruo mas lento
        "factor_luz": 1.25,                  # >1 = mas vision
        "mapa": [
            "511111111111115",
            "500050000050205",
            "501110111011105",
            "505000005300505",
            "505050501110525",
            "505053500050005",
            "505011105050505",
            "505003005050005",
            "501110111050505",
            "500000500053005",
            "511050505011105",
            "500003005000005",
            "501111111011115",
            "500000000020205",
            "511111111111115"
        ]
    },
    {
        "nombre": "Nivel 3",
        "jugador": (15, 1),
        "monstruo": (15, 13),
        # Multiplicadores de dificultad (se combinan con Facil/Normal/Dificil)
        "factor_velocidad_monstruo": 1.15,   # >1 = monstruo mas lento
        "factor_luz": 1.1,                  # >1 = mas vision
        "mapa": [
            "51111111111111115",
            "53030000005003005",
            "50111110505011105",
            "50000053500050005",
            "51105050501110115",
            "50005050505050505",
            "50111050111050505",
            "50535000530050005",
            "50521112521111105",
            "50500000500050205",
            "50111110111011105",
            "50530050005000005",
            "50505011111011105",
            "50005000000000005",
            "50111111111111115",
            "50032000202000005",
            "51111111111111115"
        ]
    },
    {
        "nombre": "Nivel 4",
        "jugador": (1, 5),
        "monstruo": (10, 5),
        # Multiplicadores de dificultad (se combinan con Facil/Normal/Dificil)
        "factor_velocidad_monstruo": 1.0,   # >1 = monstruo mas lento
        "factor_luz": 1.0,                  # >1 = mas vision
        "mapa": [
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
    },
    {
        "nombre": "Nivel 5",
        "jugador": (25, 25),
        "monstruo": (11, 19),
        # Multiplicadores de dificultad (se combinan con Facil/Normal/Dificil)
        "factor_velocidad_monstruo": 0.85,   # >1 = monstruo mas lento
        "factor_luz": 0.95,                  # >1 = mas vision
        "mapa": [
            "511111111111111111111111115",
            "502000205000005000502020005",
            "511050111011105050501111105",
            "500050005050530050005050005",
            "505050505050111011111250115",
            "505000505000000050205050205",
            "505011121110111011125011105",
            "500050000000000050005020005",
            "505050505011111052111110505",
            "500050035050035050000050505",
            "505011101110505050111050505",
            "500000500000000050500350005",
            "511111111050111110501111115",
            "500000030050500000500050005",
            "505011105050505050111050505",
            "500050005000530053005000505",
            "511050111050501110505011105",
            "500000500350005000500050005",
            "501111101110111110501110505",
            "500000500050000050005000505",
            "501110505011111050505011105",
            "530050005050035000500050005",
            "505011105050501110111050505",
            "505050500053500000500050505",
            "505052111110111111101110505",
            "500300030000000000005000005",
            "511111111111111111111111115"
        ]
    }
]

TOTAL_NIVELES = len(NIVELES)


class Nivel:

    def __init__(self, indice=0):
        self.llaves_recolectadas = 0
        self.poderes_pendientes = []
        self.matriz = []
        self.cargar(indice)

    # --- Datos del nivel actual -------------------------------------------
    @property
    def nombre(self):
        return self.datos["nombre"]

    @property
    def numero(self):
        return self.indice + 1

    @property
    def filas(self):
        return len(self.matriz)

    @property
    def columnas(self):
        return len(self.matriz[0])

    @property
    def inicio_jugador(self):
        return self.datos["jugador"]

    @property
    def inicio_monstruo(self):
        return self.datos["monstruo"]

    # --- Carga del mapa ---------------------------------------------------
    def cargar(self, indice):
        self.indice = indice
        self.datos = NIVELES[indice]
        self.llaves_recolectadas = 0
        self.poderes_pendientes = []

        self.matriz = [
            [int(char) for char in fila]
            for fila in self.datos["mapa"]
        ]

        filas = self.filas
        columnas = self.columnas
        excluidas = {self.inicio_jugador, self.inicio_monstruo}

        def libres():
            return [
                (x, y)
                for y in range(filas)
                for x in range(columnas)
                if self.matriz[y][x] == 0 and (x, y) not in excluidas
            ]

        # Colocar la salida lejos del jugador
        jx, jy = self.inicio_jugador
        distancia_min = (filas + columnas) // 3

        candidatas = [
            (x, y) for (x, y) in libres()
            if abs(x - jx) + abs(y - jy) >= distancia_min
        ]

        if not candidatas:
            candidatas = libres()

        if candidatas:
            sx, sy = random.choice(candidatas)
            self.matriz[sy][sx] = 4

        # Colocar los tres poderes
        for poder in (6, 7, 8):
            casillas = libres()

            if casillas:
                px, py = random.choice(casillas)
                self.matriz[py][px] = poder

    def reiniciar(self):
        """Reinicia el nivel actual (nueva colocacion de salida y poderes)."""
        self.cargar(self.indice)

    def bfs_pathfinding(
        self, inicio_x, inicio_y, destino_x, destino_y
    ):
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

            for dx, dy in [
                (-1, 0), (1, 0), (0, -1), (0, 1)
            ]:
                nx, ny = x + dx, y + dy

                if (
                    0 <= ny < len(self.matriz)
                    and 0 <= nx < len(self.matriz[0])
                ):
                    if (nx, ny) not in visitados:
                        casilla = self.matriz[ny][nx]

                        # El monstruo no atraviesa muros
                        # ni puertas cerradas.
                        if casilla not in (1, 5, 2):
                            visitados.add((nx, ny))
                            cola.append(
                                (nx, ny, camino + [(nx, ny)])
                            )

        return inicio_x, inicio_y
