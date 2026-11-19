# config.py
# La ventana tiene tamano fijo. Cada nivel ajusta el tamano de sus casillas
# para caber en ella (mapas mas grandes = casillas mas chicas).
TILE_SIZE = 40          # Tamano base (el del nivel 4, de 21x21)
TILE_MAX = 60           # Tamano maximo de casilla (niveles pequenos)
FILAS = 21
COLUMNAS = 21
WIDTH = COLUMNAS * TILE_SIZE
HEIGHT = FILAS * TILE_SIZE
FPS = 60

# Vidas
VIDAS_INICIALES = 3

# Paleta de Colores
NEGRO = (0, 0, 0)
GRIS = (100, 100, 100)
BLANCO = (255, 255, 255)
AZUL = (50, 150, 255)
ROJO = (255, 50, 50)
AMARILLO = (255, 200, 50)
VERDE = (50, 255, 100)
MORADO = (150, 50, 255)
# config.py (Agregar al final)
GRIS_CLARO = (200, 200, 200)

BOTON_ANCHO = 200
BOTON_ALTO = 50
BOTON_X = (WIDTH // 2) - (BOTON_ANCHO // 2)
BOTON_Y = (HEIGHT // 2) + 40
