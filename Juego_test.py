import pygame
import sys
from collections import deque

# --- CONFIGURACIÓN INICIAL ---
pygame.init()
TILE_SIZE = 40 

# Colores
NEGRO = (0, 0, 0)
GRIS = (100, 100, 100)
BLANCO = (255, 255, 255)
AZUL = (50, 150, 255)      # Jugador
ROJO = (255, 50, 50)       # Monstruo
AMARILLO = (255, 200, 50)  # Puerta Bloqueada
VERDE = (50, 255, 100)     # Llave / Fusible
MORADO = (150, 50, 255)    # SALIDA (Victoria)
GRIS_CLARO = (200, 200, 200)

# --- EL MAPA EN ANILLO (13x13) ---
# 0: Suelo, 1: Muro, 2: Puerta, 3: Llave, 4: Salida
MAPA_ORIGINAL = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 0, 0, 2, 0, 0, 0, 2, 0, 0, 3, 1], # Habitaciones Superiores
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1], 
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1], 
    [1, 1, 2, 1, 1, 1, 0, 1, 1, 1, 2, 1, 1], # Ducto central-arriba (6,4)
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # Ductos laterales (4,5) y (8,5)
    [1, 3, 0, 0, 1, 0, 0, 0, 1, 0, 0, 3, 1], # Centro: Jugador inicia en (6,6)
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # Ductos laterales (4,7) y (8,7)
    [1, 1, 2, 1, 1, 1, 0, 1, 1, 1, 2, 1, 1], # Ducto central-abajo (6,8)
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1], 
    [1, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 1], 
    [1, 3, 0, 0, 1, 0, 3, 0, 1, 0, 0, 4, 1], # SALIDA (4) en (11,11)
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

FILAS, COLUMNAS = len(MAPA_ORIGINAL), len(MAPA_ORIGINAL[0])
pantalla = pygame.display.set_mode((COLUMNAS * TILE_SIZE, FILAS * TILE_SIZE))
pygame.display.set_caption("Mansión - Fase 4: Escape y Victoria")

BOTON_ANCHO, BOTON_ALTO = 200, 50
BOTON_X = (COLUMNAS * TILE_SIZE // 2) - (BOTON_ANCHO // 2)
BOTON_Y = (FILAS * TILE_SIZE // 2) + 40
rectangulo_boton = pygame.Rect(BOTON_X, BOTON_Y, BOTON_ANCHO, BOTON_ALTO)

def reiniciar_juego():
    global mapa, jugador_x, jugador_y, monstruo_x, monstruo_y, llaves, estado_juego
    mapa = [fila[:] for fila in MAPA_ORIGINAL]
    jugador_x, jugador_y = 6, 6      # Centro
    monstruo_x, monstruo_y = 6, 1    # Arriba al centro
    llaves = 0
    estado_juego = "JUGANDO"

reiniciar_juego()

def calcular_paso_monstruo(inicio_x, inicio_y, objetivo_x, objetivo_y):
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
                # El monstruo puede pisar suelo (0), llaves (3) y la salida (4)
                if mapa[ny][nx] in [0, 3, 4] and (nx, ny) not in visitados:
                    visitados.add((nx, ny))
                    cola.append((nx, ny, camino + [(nx, ny)]))
    return (inicio_x, inicio_y)

# --- BUCLE PRINCIPAL ---
reloj = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if estado_juego in ["GAME OVER", "VICTORIA"]:
                if rectangulo_boton.collidepoint(event.pos):
                    reiniciar_juego()
            
        elif event.type == pygame.KEYDOWN and estado_juego == "JUGANDO":
            nx, ny = jugador_x, jugador_y
            
            if event.key == pygame.K_UP: ny -= 1
            elif event.key == pygame.K_DOWN: ny += 1
            elif event.key == pygame.K_LEFT: nx -= 1
            elif event.key == pygame.K_RIGHT: nx += 1
                
            movimiento_valido = False
            destino = mapa[ny][nx]
            
            if destino == 0: 
                jugador_x, jugador_y = nx, ny
                movimiento_valido = True
            elif destino == 3: 
                llaves += 1
                mapa[ny][nx] = 0
                jugador_x, jugador_y = nx, ny
                movimiento_valido = True
            elif destino == 2: 
                if llaves > 0:
                    llaves -= 1
                    mapa[ny][nx] = 0 
                    jugador_x, jugador_y = nx, ny
                    movimiento_valido = True
            elif destino == 4: # ¡PISASTE LA SALIDA!
                jugador_x, jugador_y = nx, ny
                estado_juego = "VICTORIA"
            
            # El monstruo se mueve si hiciste un movimiento válido y el juego sigue
            if movimiento_valido and estado_juego == "JUGANDO":
                monstruo_x, monstruo_y = calcular_paso_monstruo(
                    monstruo_x, monstruo_y, jugador_x, jugador_y
                )
                
            # Verifica colisión después de que ambos se mueven
            if jugador_x == monstruo_x and jugador_y == monstruo_y:
                estado_juego = "GAME OVER"

    # --- RENDERIZADO VISUAL ---
    pantalla.fill(NEGRO)
    
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            casilla = mapa[fila][col]
            rect = (col * TILE_SIZE, fila * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if casilla == 1: pygame.draw.rect(pantalla, GRIS, rect)
            elif casilla == 2: pygame.draw.rect(pantalla, AMARILLO, rect)
            elif casilla == 3: pygame.draw.rect(pantalla, VERDE, rect)
            elif casilla == 4: pygame.draw.rect(pantalla, MORADO, rect) # Salida
                
    if estado_juego == "JUGANDO":
        pygame.draw.rect(pantalla, ROJO, (monstruo_x * TILE_SIZE, monstruo_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(pantalla, AZUL, (jugador_x * TILE_SIZE, jugador_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
    elif estado_juego in ["GAME OVER", "VICTORIA"]:
        fuente_grande = pygame.font.SysFont(None, 48)
        if estado_juego == "GAME OVER":
            texto_fin = fuente_grande.render("¡TE ATRAPARON!", True, ROJO)
        else:
            texto_fin = fuente_grande.render("¡ESCAPASTE!", True, VERDE)
            
        pantalla.blit(texto_fin, (COLUMNAS*TILE_SIZE//2 - 140, FILAS*TILE_SIZE//2 - 40))
        
        pygame.draw.rect(pantalla, GRIS_CLARO, rectangulo_boton)
        pygame.draw.rect(pantalla, BLANCO, rectangulo_boton, 3) 
        
        fuente_chica = pygame.font.SysFont(None, 36)
        texto_boton = fuente_chica.render("Jugar de nuevo", True, NEGRO)
        pantalla.blit(texto_boton, (BOTON_X + 15, BOTON_Y + 12))

    pygame.display.flip()
    reloj.tick(30)