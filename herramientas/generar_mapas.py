"""
Generador de mapas para Escape de la Mazmorra.

Crea laberintos con ciclos (para poder esquivar al monstruo), coloca
puertas en pasillos que de verdad bloquean zonas, reparte las llaves y
VALIDA que el mapa se pueda completar en cualquier orden en que el jugador
abra puertas (nunca se queda sin llaves atrapado).
"""
import random
import sys
from collections import deque

VECINOS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def generar_laberinto(n, prob_ciclos, rng):
    # 1 = pared, 0 = pasillo. Celdas en coordenadas impares.
    g = [[1] * n for _ in range(n)]
    celdas = [(r, c) for r in range(1, n, 2) for c in range(1, n, 2)]
    inicio = rng.choice(celdas)
    g[inicio[0]][inicio[1]] = 0
    pila = [inicio]
    while pila:
        r, c = pila[-1]
        opciones = []
        for dc, dr in VECINOS:
            nr, nc = r + dr * 2, c + dc * 2
            if 1 <= nr < n - 1 and 1 <= nc < n - 1 and g[nr][nc] == 1:
                opciones.append((nr, nc, r + dr, c + dc))
        if opciones:
            nr, nc, pr, pc = rng.choice(opciones)
            g[pr][pc] = 0
            g[nr][nc] = 0
            pila.append((nr, nc))
        else:
            pila.pop()

    # Abrir paredes extra para crear ciclos
    for r in range(1, n - 1):
        for c in range(1, n - 1):
            es_borde_celda = (r % 2) != (c % 2)  # pared entre dos celdas
            if es_borde_celda and g[r][c] == 1 and rng.random() < prob_ciclos:
                g[r][c] = 0
    return g


def vecinos_libres(g, r, c):
    n = len(g)
    for dc, dr in VECINOS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n and g[nr][nc] != 1:
            yield nr, nc


def bfs_dist(g, inicio):
    d = {inicio: 0}
    q = deque([inicio])
    while q:
        r, c = q.popleft()
        for nr, nc in vecinos_libres(g, r, c):
            if (nr, nc) not in d:
                d[(nr, nc)] = d[(r, c)] + 1
                q.append((nr, nc))
    return d


def puentes(g, inicio):
    """Casillas de pasillo (entre celdas) cuya eliminacion desconecta el mapa."""
    total = len(bfs_dist(g, inicio))
    res = []
    n = len(g)
    for r in range(1, n - 1):
        for c in range(1, n - 1):
            if g[r][c] == 0 and (r % 2) != (c % 2):
                g[r][c] = 1
                if len(bfs_dist(g, inicio)) < total - 1:
                    res.append((r, c))
                g[r][c] = 0
    return res


def region(m, inicio, abiertas):
    vis = {inicio}
    q = deque([inicio])
    while q:
        r, c = q.popleft()
        for nr, nc in vecinos_libres(m, r, c):
            if (nr, nc) in vis:
                continue
            if m[nr][nc] == 2 and (nr, nc) not in abiertas:
                continue
            vis.add((nr, nc))
            q.append((nr, nc))
    return vis


def es_resoluble(m, inicio, limite_estados=150000):
    """
    Explora TODAS las formas de gastar llaves. El mapa es valido si en
    ningun caso el jugador se queda sin poder alcanzar alguna casilla.
    """
    n = len(m)
    objetivo = {
        (r, c) for r in range(n) for c in range(n) if m[r][c] in (0, 3)
    }
    vistos = set()
    pila = [frozenset()]
    while pila:
        abiertas = pila.pop()
        if abiertas in vistos:
            continue
        vistos.add(abiertas)
        if len(vistos) > limite_estados:
            return False
        reg = region(m, inicio, abiertas)
        llaves = sum(1 for (r, c) in reg if m[r][c] == 3)
        disponibles = llaves - len(abiertas)
        puertas_ady = set()
        for (r, c) in reg:
            for nr, nc in vecinos_libres(m, r, c):
                if m[nr][nc] == 2 and (nr, nc) not in abiertas:
                    puertas_ady.add((nr, nc))
        if disponibles > 0 and puertas_ady:
            for p in puertas_ady:
                pila.append(abiertas | {p})
        else:
            # Estado final: debe haber visitado todo el mapa
            if not objetivo <= reg:
                return False
    return True


def construir(n, prob_ciclos, num_puertas, num_llaves, esquina, semilla):
    rng = random.Random(semilla)
    inicio = {
        "TL": (1, 1), "TR": (1, n - 2), "BL": (n - 2, 1), "BR": (n - 2, n - 2),
    }[esquina]  # (fila, col)

    for intento in range(3000):
        g = generar_laberinto(n, prob_ciclos, rng)
        cand = puentes(g, inicio)
        # Preferir puentes que encierran bastante mapa
        if len(cand) < num_puertas:
            continue
        rng.shuffle(cand)
        puertas = cand[:num_puertas]
        m = [fila[:] for fila in g]
        for (r, c) in puertas:
            m[r][c] = 2

        reg0 = region(m, inicio, frozenset())
        celdas0 = [p for p in reg0 if p[0] % 2 == 1 and p[1] % 2 == 1 and p != inicio]
        todas = [(r, c) for r in range(1, n, 2) for c in range(1, n, 2) if (r, c) != inicio]

        k0 = max(2, num_llaves // 3)
        if len(celdas0) < k0:
            continue
        llaves = rng.sample(celdas0, k0)
        resto = [p for p in todas if p not in llaves]
        llaves += rng.sample(resto, num_llaves - k0)
        for (r, c) in llaves:
            m[r][c] = 3

        if es_resoluble(m, inicio):
            # Posicion del monstruo: celda de la zona inicial, a distancia media
            dist = bfs_dist(
                [[1 if v in (1, 2) else 0 for v in fila] for fila in m], inicio
            )
            mx = max(dist.values())
            monstruo_cands = [
                p for p, d in dist.items()
                if p[0] % 2 == 1 and p[1] % 2 == 1 and m[p[0]][p[1]] == 0
                and mx * 0.35 <= d <= mx * 0.6
            ]
            if not monstruo_cands:
                continue
            mr, mc = rng.choice(monstruo_cands)
            return m, inicio, (mr, mc), intento
    raise RuntimeError("No se pudo generar el mapa")


def a_cadenas(m):
    n = len(m)
    out = []
    for r in range(n):
        fila = ""
        for c in range(n):
            v = m[r][c]
            if r in (0, n - 1) or c in (0, n - 1):
                if (r in (0, n - 1)) and (c in (0, n - 1)):
                    fila += "5"
                elif r in (0, n - 1):
                    fila += "1"
                else:
                    fila += "5"
            elif v == 1:
                if r % 2 == 1 and c % 2 == 0:
                    fila += "5"
                elif r % 2 == 0 and c % 2 == 1:
                    fila += "1"
                else:  # pilar
                    izq = m[r][c - 1] == 1
                    der = m[r][c + 1] == 1
                    fila += "1" if (izq or der) else "5"
            else:
                fila += str(v)
        out.append(fila)
    return out


CONFIG = {
    # nombre: (tam, ciclos, puertas, llaves, esquina, semilla)
    1: (11, 0.30, 2, 3, "TL", 11),
    2: (15, 0.25, 4, 5, "BL", 22),
    3: (17, 0.20, 7, 8, "TR", 33),
    5: (27, 0.15, 12, 13, "BR", 55),
}

if __name__ == "__main__":
    resultado = {}
    for nivel, cfg in CONFIG.items():
        m, ini, mon, intentos = construir(*cfg)
        cad = a_cadenas(m)
        resultado[nivel] = (cad, ini, mon)
        print(f"# Nivel {nivel}: {len(cad)}x{len(cad)}  intentos={intentos}  "
              f"jugador(x,y)=({ini[1]},{ini[0]})  monstruo(x,y)=({mon[1]},{mon[0]})",
              file=sys.stderr)
    import json
    print(json.dumps({k: {"mapa": v[0], "jugador": [v[1][1], v[1][0]],
                          "monstruo": [v[2][1], v[2][0]]}
                      for k, v in resultado.items()}))
 