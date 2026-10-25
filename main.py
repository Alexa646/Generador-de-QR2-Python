"""
=====================================================================
 GENERADOR DE MATRIZ QR (Versión 2 = 25x25, modo Byte, nivel M)
=====================================================================
 Etapas implementadas (según la rúbrica):
   FASE 1 -> Inserción de los bits de datos en zigzag
   FASE 2 -> Corrección de errores Reed-Solomon
   FASE 3 -> Enmascaramiento y matriz final (con bits de formato)

 Convención de la matriz:
   1 = módulo negro | 0 = módulo blanco
   None = celda libre (aún sin dato) | 'F' = reservada para formato
=====================================================================
"""

DiccionarioDEC = {
    # Números
    '0': 48, '1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 54, '7': 55, '8': 56, '9': 57,
    # Mayúsculas
    'A': 65, 'B': 66, 'C': 67, 'D': 68, 'E': 69, 'F': 70, 'G': 71, 'H': 72, 'I': 73, 'J': 74,
    'K': 75, 'L': 76, 'M': 77, 'N': 78, 'O': 79, 'P': 80, 'Q': 81, 'R': 82, 'S': 83, 'T': 84,
    'U': 85, 'V': 86, 'W': 87, 'X': 88, 'Y': 89, 'Z': 90,
    # Minúsculas
    'a': 97, 'b': 98, 'c': 99, 'd': 100, 'e': 101, 'f': 102, 'g': 103, 'h': 104, 'i': 105,
    'j': 106, 'k': 107, 'l': 108, 'm': 109, 'n': 110, 'o': 111, 'p': 112, 'q': 113, 'r': 114,
    's': 115, 't': 116, 'u': 117, 'v': 118, 'w': 119, 'x': 120, 'y': 121, 'z': 122,
    # Símbolos QR especiales
    ' ': 32, '$': 36, '%': 37, '*': 42, '+': 43, '-': 45, '.': 46, '/': 47, ':': 58
}

DiccionarioHEX = {
    # Números
    '0': '30', '1': '31', '2': '32', '3': '33', '4': '34', '5': '35', '6': '36', '7': '37', '8': '38', '9': '39',
    # Mayúsculas
    'A': '41', 'B': '42', 'C': '43', 'D': '44', 'E': '45', 'F': '46', 'G': '47', 'H': '48', 'I': '49', 'J': '4A',
    'K': '4B', 'L': '4C', 'M': '4D', 'N': '4E', 'O': '4F', 'P': '50', 'Q': '51', 'R': '52', 'S': '53', 'T': '54',
    'U': '55', 'V': '56', 'W': '57', 'X': '58', 'Y': '59', 'Z': '5A',
    # Minúsculas
    'a': '61', 'b': '62', 'c': '63', 'd': '64', 'e': '65', 'f': '66', 'g': '67', 'h': '68', 'i': '69',
    'j': '6A', 'k': '6B', 'l': '6C', 'm': '6D', 'n': '6E', 'o': '6F', 'p': '70', 'q': '71', 'r': '72',
    's': '73', 't': '74', 'u': '75', 'v': '76', 'w': '77', 'x': '78', 'y': '79', 'z': '7A',
    # Símbolos QR especiales
    ' ': '20', '$': '24', '%': '25', '*': '2A', '+': '2B', '-': '2D', '.': '2E', '/': '2F', ':': '3A'
}

DiccionarioBIN = {
    # Números
    '0': '00110000', '1': '00110001', '2': '00110010', '3': '00110011', '4': '00110100',
    '5': '00110101', '6': '00110110', '7': '00110111', '8': '00111000', '9': '00111001',
    # Mayúsculas
    'A': '01000001', 'B': '01000010', 'C': '01000011', 'D': '01000100', 'E': '01000101',
    'F': '01000110', 'G': '01000111', 'H': '01001000', 'I': '01001001', 'J': '01001010',
    'K': '01001011', 'L': '01001100', 'M': '01001101', 'N': '01001110', 'O': '01001111',
    'P': '01010000', 'Q': '01010001', 'R': '01010010', 'S': '01010011', 'T': '01010100',
    'U': '01010101', 'V': '01010110', 'W': '01010111', 'X': '01011000', 'Y': '01011001', 'Z': '01011010',
    # Minúsculas
    'a': '01100001', 'b': '01100010', 'c': '01100011', 'd': '01100100', 'e': '01100101',
    'f': '01100110', 'g': '01100111', 'h': '01101000', 'i': '01101001', 'j': '01101010',
    'k': '01101011', 'l': '01101100', 'm': '01101101', 'n': '01101110', 'o': '01101111',
    'p': '01110000', 'q': '01110001', 'r': '01110010', 's': '01110011', 't': '01110100',
    'u': '01110101', 'v': '01110110', 'w': '01110111', 'x': '01111000', 'y': '01111001', 'z': '01111010',
    # Símbolos QR especiales
    ' ': '00100000', '$': '00100100', '%': '00100101', '*': '00101010', '+': '00101011',
    '-': '00101101', '.': '00101110', '/': '00101111', ':': '00111010'
}


#Validar caracteres permitidos por la norma QR
def validar_caracteres_qr(texto: str) -> bool:
    permitidos = set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:")
    return all(caracter in permitidos for caracter in texto.upper())

#Convertidor de caractertes
def convertidor_Caracter(texto: str):
    vector_dec = [DiccionarioDEC[caracter] for caracter in texto if caracter in DiccionarioDEC]
    vector_hex = [DiccionarioHEX[caracter] for caracter in texto if caracter in DiccionarioHEX]
    vector_bin = [DiccionarioBIN[caracter] for caracter in texto if caracter in DiccionarioBIN]

    return {
        "DEC": vector_dec,
        "HEX": vector_hex,
        "BIN": vector_bin,
        "CADENA_BIN": "".join(vector_bin)
    }


# =====================================================================
#  PARÁMETROS DEL QR (Versión 2, nivel de corrección M)
# =====================================================================
SIZE = 25                 # Versión 2 -> 21 + 4*(2-1) = 25 módulos por lado
VERSION = 2
EC_LEVEL = "M"
# Tabla de la norma para versión 2 (1 solo bloque):
#   nivel -> palabras de datos | palabras de corrección (total = 44)
EC_DATA_CODEWORDS = {"L": 34, "M": 28, "Q": 22, "H": 16}[EC_LEVEL]
EC_CODEWORDS = {"L": 10, "M": 16, "Q": 22, "H": 28}[EC_LEVEL]
EC_LEVEL_BITS = {"L": "01", "M": "00", "Q": "11", "H": "10"}[EC_LEVEL]
TOTAL_CODEWORDS = EC_DATA_CODEWORDS + EC_CODEWORDS   # 44
REMAINDER_BITS = 7        # Bits sobrantes de la versión 2 (359 celdas - 44*8)
# Capacidad: 4 bits modo + 8 bits longitud + 8n bits datos + 4 bits terminador
MAX_CARACTERES = 25


# =====================================================================
#  FASE 2 (herramientas): ARITMÉTICA EN GF(256) Y REED-SOLOMON
# =====================================================================
# Reed-Solomon trabaja con bytes interpretados como elementos del campo
# finito GF(2^8). En el QR el campo se define con el polinomio primitivo
#       x^8 + x^4 + x^3 + x^2 + 1   (0x11D)
# y el elemento primitivo es alfa = 2.
#  - SUMA y RESTA son un XOR.
#  - MULTIPLICACIÓN: a*b = alfa^(log a + log b)  (usamos tablas EXP/LOG).
EXP = [0] * 512   # EXP[i] = alfa^i   (duplicada para evitar el módulo 255)
LOG = [0] * 256   # LOG[x] = i tal que alfa^i = x


def _init_gf():
    x = 1
    for i in range(255):
        EXP[i] = x
        LOG[x] = i
        x <<= 1                 # multiplicar por alfa = desplazar 1 bit
        if x & 0x100:           # si se sale de 8 bits, reducir con 0x11D
            x ^= 0x11D
    for i in range(255, 512):
        EXP[i] = EXP[i - 255]


_init_gf()


def gf_mul(a, b):
    """Multiplicación en GF(256)."""
    if a == 0 or b == 0:
        return 0
    return EXP[LOG[a] + LOG[b]]


def poly_mul(p, q):
    """Producto de dos polinomios con coeficientes en GF(256)."""
    r = [0] * (len(p) + len(q) - 1)
    for i, pc in enumerate(p):
        for j, qc in enumerate(q):
            r[i + j] ^= gf_mul(pc, qc)
    return r


def rs_generator_poly(nsym):
    """
    Polinomio generador de grado nsym:
        g(x) = (x - a^0)(x - a^1)...(x - a^(nsym-1))
    Como en GF(2^8) restar = sumar, cada factor es (x + a^i).
    Devuelve los coeficientes de mayor a menor grado.
    """
    g = [1]
    for i in range(nsym):
        g = poly_mul(g, [1, EXP[i]])
    return g


def rs_encode(data_codewords, nsym, traza=0):
    """
    Calcula las 'nsym' palabras de corrección de errores.
    Idea matemática: las EC son el RESTO de dividir
          M(x) * x^nsym   entre   g(x)
    donde M(x) es el polinomio formado por los bytes de datos.
    Se hace una división larga: en cada paso se toma el coeficiente líder,
    se multiplica g(x) por él y se resta (XOR) del dividendo.
    'traza' = cuántos pasos imprimir para documentar el proceso.
    """
    gen = rs_generator_poly(nsym)
    res = list(data_codewords) + [0] * nsym        # M(x) * x^nsym
    for i in range(len(data_codewords)):
        coef = res[i]                              # coeficiente líder actual
        if coef != 0:
            for j in range(len(gen)):
                res[i + j] ^= gf_mul(gen[j], coef)  # restar coef * g(x)
        if i < traza:
            print(f"   Paso {i + 1}: coeficiente líder = {coef:>3} -> "
                  f"se resta {coef} * g(x). Resultado parcial: {res[i + 1:]}")
    return res[len(data_codewords):]               # el resto = bytes EC


def validar_reed_solomon_ejemplo_conocido():
    """
    Validación con un ejemplo publicado en la literatura QR:
    'HELLO WORLD', versión 1-M (16 palabras de datos, 10 de corrección).
    """
    datos = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17]
    esperado = [196, 35, 39, 119, 235, 215, 231, 226, 93, 23]
    obtenido = rs_encode(datos, 10)
    gen_esperado = [0, 251, 67, 46, 61, 118, 70, 64, 94, 32, 45]   # exponentes de alfa
    gen_obtenido = [LOG[c] for c in rs_generator_poly(10)]
    return obtenido == esperado and gen_obtenido == gen_esperado, datos, esperado, obtenido


# =====================================================================
#  CODIFICACIÓN DE DATOS (modo Byte) -> palabras de datos
# =====================================================================
def codificar_datos(texto):
    """
    Estructura del flujo de datos:
      [modo 4 bits][longitud 8 bits][datos 8n bits][terminador][relleno]
    Devuelve la lista de 'EC_DATA_CODEWORDS' bytes (palabras de datos).
    """
    if len(texto) > MAX_CARACTERES:
        raise ValueError(f"Máximo {MAX_CARACTERES} caracteres para versión {VERSION}-{EC_LEVEL}")

    modo = "0100"                                  # indicador de modo Byte
    longitud = format(len(texto), "08b")           # contador (8 bits en versiones 1-9)
    datos = "".join(conseguir_valor_bin(texto))    # ASCII en binario
    bits = modo + longitud + datos

    capacidad_bits = EC_DATA_CODEWORDS * 8
    bits += "0" * min(4, capacidad_bits - len(bits))    # terminador (hasta 4 ceros)
    bits += "0" * ((8 - len(bits) % 8) % 8)             # completar a múltiplo de 8

    palabras = [int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)]

    # Relleno alternado exigido por la norma: 11101100 (236) y 00010001 (17)
    pad = [0xEC, 0x11]
    i = 0
    while len(palabras) < EC_DATA_CODEWORDS:
        palabras.append(pad[i % 2])
        i += 1
    return palabras


def palabras_a_bits(palabras):
    return "".join(format(p, "08b") for p in palabras)


# =====================================================================
#  FASE 1: MATRIZ BASE (módulos funcionales) Y ZIGZAG
# =====================================================================
def crear_matriz(tam=SIZE):
    """Matriz vacía: None = celda libre."""
    return [[None for _ in range(tam)] for _ in range(tam)]


def colocar_patron_posicion(matriz, fila, col):
    """Finder 7x7: borde negro, anillo blanco, núcleo negro 3x3."""
    for i in range(7):
        for j in range(7):
            en_borde = i in (0, 6) or j in (0, 6)
            en_nucleo = 2 <= i <= 4 and 2 <= j <= 4
            matriz[fila + i][col + j] = 1 if (en_borde or en_nucleo) else 0


def colocar_finders(matriz):
    tam = len(matriz)
    colocar_patron_posicion(matriz, 0, 0)            # superior-izquierda
    colocar_patron_posicion(matriz, 0, tam - 7)      # superior-derecha
    colocar_patron_posicion(matriz, tam - 7, 0)      # inferior-izquierda


def colocar_separadores(matriz):
    """Anillo blanco de 1 módulo alrededor de cada finder."""
    tam = len(matriz)
    esquinas = [(0, 0), (0, tam - 7), (tam - 7, 0)]
    for (fr, fc) in esquinas:
        for i in range(-1, 8):
            for j in range(-1, 8):
                r, c = fr + i, fc + j
                if 0 <= r < tam and 0 <= c < tam and (i in (-1, 7) or j in (-1, 7)):
                    if matriz[r][c] is None:
                        matriz[r][c] = 0


def colocar_timing(matriz):
    """Líneas de sincronización alternadas (fila 6 y columna 6)."""
    tam = len(matriz)
    for i in range(8, tam - 8):
        valor = 1 if i % 2 == 0 else 0
        if matriz[6][i] is None:
            matriz[6][i] = valor
        if matriz[i][6] is None:
            matriz[i][6] = valor


def colocar_alineacion(matriz, fila_centro=18, col_centro=18):
    """Patrón de alineación 5x5 (versión 2: un solo patrón centrado en (18,18))."""
    for i in range(-2, 3):
        for j in range(-2, 3):
            r, c = fila_centro + i, col_centro + j
            if abs(i) == 2 or abs(j) == 2 or (i == 0 and j == 0):
                matriz[r][c] = 1
            else:
                matriz[r][c] = 0


def colocar_modulo_oscuro(matriz):
    """Módulo fijo SIEMPRE negro en la fila 4*versión + 9, columna 8."""
    matriz[4 * VERSION + 9][8] = 1


def reservar_zona_formato(matriz):
    """Marca con 'F' las celdas que después llevarán los 15 bits de formato."""
    tam = len(matriz)
    for i in range(9):
        if matriz[8][i] is None:
            matriz[8][i] = 'F'
        if matriz[i][8] is None:
            matriz[i][8] = 'F'
    for i in range(8):
        if matriz[8][tam - 1 - i] is None:
            matriz[8][tam - 1 - i] = 'F'
        if matriz[tam - 1 - i][8] is None:
            matriz[tam - 1 - i][8] = 'F'


def construir_matriz_base(tam=SIZE):
    """Matriz inicializada con TODOS los módulos reservados/funcionales."""
    matriz = crear_matriz(tam)
    colocar_finders(matriz)
    colocar_separadores(matriz)
    colocar_timing(matriz)
    colocar_alineacion(matriz)
    colocar_modulo_oscuro(matriz)
    reservar_zona_formato(matriz)
    return matriz


def recorrido_zigzag(tam):
    """
    Generador del ORDEN de lectura/escritura que define la norma:
      1. Se empieza en la esquina inferior derecha.
      2. Se avanza en franjas verticales de 2 columnas, de derecha a izquierda.
      3. Dentro de una franja se visita primero la columna derecha y luego la
         izquierda de cada fila (forma de zigzag).
      4. La primera franja SUBE; cada franja siguiente alterna (baja, sube...).
      5. La columna 6 (timing vertical) se omite por completo.
    """
    col = tam - 1
    subir = True
    while col > 0:
        if col == 6:                 # columna reservada: se salta (sin alternar)
            col -= 1
            continue
        filas = range(tam - 1, -1, -1) if subir else range(0, tam)
        for fila in filas:
            for c in (col, col - 1):     # derecha primero, luego izquierda
                yield fila, c
        subir = not subir            # alternar dirección vertical
        col -= 2                     # siguiente franja de 2 columnas


def insertar_datos_zigzag(matriz, cadena_bits, rellenar_resto=True):
    """
    Inserta los bits siguiendo 'recorrido_zigzag', pero SOLO en celdas libres
    (None). Así se respetan Finder, Separadores, Timing, Alineación y Formato.
    rellenar_resto=False deja vacías (None) las celdas que sobren; se usa para
    mostrar la matriz de la Fase 1 (solo datos, antes de Reed-Solomon).
    Devuelve cuántos bits se insertaron.
    """
    idx = 0
    for fila, c in recorrido_zigzag(len(matriz)):
        if matriz[fila][c] is not None:       # módulo reservado -> se omite
            continue
        if idx < len(cadena_bits):
            matriz[fila][c] = int(cadena_bits[idx])
            idx += 1
        elif rellenar_resto:
            matriz[fila][c] = 0
    return idx


# =====================================================================
#  FASE 3: ENMASCARAMIENTO
# =====================================================================
# La máscara invierte (XOR 1) los módulos donde la condición es verdadera.
# (r = fila, c = columna). Se aplica SOLO a módulos de datos y EC.
MASK_FORMULAS = [
    "(r + c) mod 2 == 0",
    "r mod 2 == 0",
    "c mod 3 == 0",
    "(r + c) mod 3 == 0",
    "(r//2 + c//3) mod 2 == 0",
    "(r*c) mod 2 + (r*c) mod 3 == 0",
    "((r*c) mod 2 + (r*c) mod 3) mod 2 == 0",
    "((r+c) mod 2 + (r*c) mod 3) mod 2 == 0",
]

MASK_FUNCS = [
    lambda r, c: (r + c) % 2 == 0,
    lambda r, c: r % 2 == 0,
    lambda r, c: c % 3 == 0,
    lambda r, c: (r + c) % 3 == 0,
    lambda r, c: (r // 2 + c // 3) % 2 == 0,
    lambda r, c: (r * c) % 2 + (r * c) % 3 == 0,
    lambda r, c: ((r * c) % 2 + (r * c) % 3) % 2 == 0,
    lambda r, c: ((r + c) % 2 + (r * c) % 3) % 2 == 0,
]


def es_celda_dato(matriz_base, r, c):
    """Una celda es de datos si en la matriz base seguía libre (None)."""
    return matriz_base[r][c] is None


def aplicar_mascara(matriz_datos, matriz_base, mask_id):
    """Devuelve una COPIA con la máscara aplicada solo a módulos de datos/EC."""
    tam = len(matriz_datos)
    resultado = [fila[:] for fila in matriz_datos]
    f = MASK_FUNCS[mask_id]
    for r in range(tam):
        for c in range(tam):
            if es_celda_dato(matriz_base, r, c) and f(r, c):
                resultado[r][c] ^= 1
    return resultado


def verificar_modulos_funcionales(antes, despues, matriz_base):
    """Cuenta cuántos módulos funcionales cambiaron por la máscara (debe ser 0)."""
    alterados = 0
    for r in range(len(antes)):
        for c in range(len(antes)):
            if not es_celda_dato(matriz_base, r, c) and antes[r][c] != despues[r][c]:
                alterados += 1
    return alterados


# ---- Penalización (4 reglas oficiales) para elegir la mejor máscara ----
_PATRON_A = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0]
_PATRON_B = [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1]


def _contar_patron_finder(linea):
    n = 0
    for i in range(len(linea) - 10):
        segmento = linea[i:i + 11]
        if segmento == _PATRON_A or segmento == _PATRON_B:
            n += 1
    return n


def penalizacion(matriz):
    tam = len(matriz)
    m = [[1 if v == 1 else 0 for v in fila] for fila in matriz]
    columnas = [[m[r][c] for r in range(tam)] for c in range(tam)]
    score = 0

    # Regla 1: 5 o más módulos iguales consecutivos (filas y columnas)
    for lineas in (m, columnas):
        for linea in lineas:
            i = 0
            while i < tam:
                n = 1
                while i + n < tam and linea[i + n] == linea[i]:
                    n += 1
                if n >= 5:
                    score += 3 + (n - 5)
                i += n

    # Regla 2: bloques 2x2 del mismo color
    for r in range(tam - 1):
        for c in range(tam - 1):
            if m[r][c] == m[r][c + 1] == m[r + 1][c] == m[r + 1][c + 1]:
                score += 3

    # Regla 3: patrón parecido a un finder (1:1:3:1:1 con 4 blancos al lado)
    for lineas in (m, columnas):
        for linea in lineas:
            score += 40 * _contar_patron_finder(linea)

    # Regla 4: balance de negros/blancos (10 puntos por cada 5% de desviación)
    negros = sum(sum(fila) for fila in m)
    porcentaje = negros * 100 / (tam * tam)
    anterior = int(porcentaje // 5) * 5
    desviacion = min(abs(anterior - 50), abs(anterior + 5 - 50))
    score += (desviacion // 5) * 10
    return score


# =====================================================================
#  INFORMACIÓN DE FORMATO (nivel EC + máscara, protegida con BCH)
# =====================================================================
def bch_formato(data5):
    """
    data5 = 2 bits de nivel EC + 3 bits de máscara.
    Se calcula el resto de dividir (data5 * x^10) entre el generador BCH
    10100110111 y se pega a los 5 bits. Luego se hace XOR con
    101010000010010 (norma) para evitar una cadena toda en ceros.
    """
    g = 0b10100110111
    d = data5 << 10
    for i in range(14, 9, -1):
        if d & (1 << i):
            d ^= g << (i - 10)
    formato = (data5 << 10) | d
    return formato ^ 0b101010000010010


def colocar_formato(matriz, mask_id):
    """Escribe los 15 bits de formato en sus DOS copias dentro de la matriz."""
    data5 = int(EC_LEVEL_BITS + format(mask_id, "03b"), 2)
    bits = format(bch_formato(data5), "015b")
    tam = len(matriz)
    copia1 = [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 7), (8, 8),
              (7, 8), (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8)]
    copia2 = [(tam - 1, 8), (tam - 2, 8), (tam - 3, 8), (tam - 4, 8), (tam - 5, 8),
              (tam - 6, 8), (tam - 7, 8),
              (8, tam - 8), (8, tam - 7), (8, tam - 6), (8, tam - 5),
              (8, tam - 4), (8, tam - 3), (8, tam - 2), (8, tam - 1)]
    for i, bit in enumerate(bits):
        r, c = copia1[i]
        matriz[r][c] = int(bit)
        r, c = copia2[i]
        matriz[r][c] = int(bit)


def elegir_mejor_mascara(matriz_datos, matriz_base):
    """
    Prueba las 8 máscaras. Para cada una: aplica la máscara, coloca los bits
    de formato correspondientes y calcula la penalización. Gana la menor.
    Devuelve (id_mascara, lista_de_puntajes, matriz_final).
    """
    puntajes = []
    mejor = None
    for mask_id in range(8):
        candidata = aplicar_mascara(matriz_datos, matriz_base, mask_id)
        colocar_formato(candidata, mask_id)
        s = penalizacion(candidata)
        puntajes.append(s)
        if mejor is None or s < mejor[0]:
            mejor = (s, mask_id, candidata)
    return mejor[1], puntajes, mejor[2]


# =====================================================================
#  PIPELINE COMPLETO POR ETAPAS (guarda la evidencia de cada fase)
# =====================================================================
def generar_qr_por_etapas(texto):
    base = construir_matriz_base()

    # --- Fase 1: solo datos ---
    palabras_datos = codificar_datos(texto)
    bits_datos = palabras_a_bits(palabras_datos)
    matriz_fase1 = [f[:] for f in base]
    bits_insertados_f1 = insertar_datos_zigzag(matriz_fase1, bits_datos, rellenar_resto=False)

    # --- Fase 2: datos + Reed-Solomon ---
    palabras_ec = rs_encode(palabras_datos, EC_CODEWORDS)
    todas = palabras_datos + palabras_ec                       # concatenación
    bits_finales = palabras_a_bits(todas) + "0" * REMAINDER_BITS
    matriz_fase2 = [f[:] for f in base]
    insertar_datos_zigzag(matriz_fase2, bits_finales)

    # --- Fase 3: máscara ---
    mask_id, puntajes, matriz_final = elegir_mejor_mascara(matriz_fase2, base)
    solo_mascara = aplicar_mascara(matriz_fase2, base, mask_id)  # sin formato (para comparar)

    return {
        "base": base,
        "palabras_datos": palabras_datos, "palabras_ec": palabras_ec, "todas": todas,
        "bits_datos": bits_datos, "bits_finales": bits_finales,
        "matriz_fase1": matriz_fase1, "bits_insertados_f1": bits_insertados_f1,
        "matriz_fase2": matriz_fase2,
        "mask_id": mask_id, "puntajes": puntajes,
        "solo_mascara": solo_mascara, "matriz_final": matriz_final,
    }


# =====================================================================
#  IMPRESIÓN / EVIDENCIA GRÁFICA EN TERMINAL
# =====================================================================
def imprimir_matriz(matriz, base=None, margen=4):
    """
    Sin 'base': QR escaneable (██ negro / blanco) con zona de silencio.
    Con 'base' (modo evidencia): distingue los tipos de módulo:
        ██ / (blanco)  módulo funcional (finder, timing, alineación...)
        ▓▓ / ░░        bit de DATO = 1 / 0
        ··             celda libre aún sin dato (esperando Reed-Solomon)
        FF             celda reservada para formato (aún sin escribir)
    """
    tam = len(matriz)
    linea_blanca = "  " * (tam + margen * 2)
    for _ in range(margen):
        print(linea_blanca)
    for r, fila in enumerate(matriz):
        partes = []
        for c, v in enumerate(fila):
            if v is None:
                partes.append("··")
            elif v == 'F':
                partes.append("FF")
            elif base is not None and base[r][c] is None:        # módulo de datos
                partes.append("▓▓" if v == 1 else "░░")
            else:                                                # módulo funcional
                partes.append("██" if v == 1 else "  ")
        print("  " * margen + "".join(partes) + "  " * margen)
    for _ in range(margen):
        print(linea_blanca)


def imprimir_orden_zigzag(base):
    """
    Evidencia del recorrido: cada celda de datos muestra el NÚMERO DE PALABRA
    (byte) al que pertenece. 00-27 = datos, 28-43 = corrección (EC),
    '--' = 7 bits sobrantes. Se aprecia el zigzag y la alternancia sube/baja.
    """
    tam = len(base)
    orden = {}
    k = 0
    for fila, c in recorrido_zigzag(tam):
        if base[fila][c] is None:
            orden[(fila, c)] = k
            k += 1
    for r in range(tam):
        partes = []
        for c in range(tam):
            if (r, c) in orden:
                palabra = orden[(r, c)] // 8
                partes.append(f"{palabra:02d} " if palabra < TOTAL_CODEWORDS else "-- ")
            elif base[r][c] == 'F':
                partes.append("FF ")
            else:
                partes.append("███" if base[r][c] == 1 else "   ")
        print("".join(partes))


def _bytes_a_texto(palabras):
    return " ".join(f"{p:>3}" for p in palabras)


# ---------------------------- FASE 1 ----------------------------------
def mostrar_fase1(texto):
    e = generar_qr_por_etapas(texto)
    base = e["base"]
    tam = len(base)
    libres = sum(1 for r in range(tam) for c in range(tam) if base[r][c] is None)
    reservadas = tam * tam - libres

    print(f"Matriz: {tam}x{tam} = {tam * tam} módulos")
    print(f"Módulos reservados : {reservadas}")
    print(f"Módulos libres     : {libres}  (= {TOTAL_CODEWORDS}*8 + {REMAINDER_BITS} bits sobrantes)")
    print(f"Palabras de datos  : {EC_DATA_CODEWORDS} ({EC_DATA_CODEWORDS * 8} bits)")
    print(f"Bits insertados    : {e['bits_insertados_f1']}  -> quedan {libres - e['bits_insertados_f1']} libres para EC\n")
    print(f"Texto: '{texto}'")
    print(f"Palabras de datos (DEC): {_bytes_a_texto(e['palabras_datos'])}")
    print(f"Cadena de {len(e['bits_datos'])} bits:\n{e['bits_datos']}\n")

    print("Matriz con SOLO datos  (▓▓=1 dato, ░░=0 dato, ··=libre, FF=formato reservado):")
    imprimir_matriz(e["matriz_fase1"], base=base, margen=1)

    print("\nOrden del zigzag (número de palabra por celda; 00-27 datos, 28-43 EC, -- sobrantes):")
    imprimir_orden_zigzag(base)


# ---------------------------- FASE 2 ----------------------------------
def mostrar_fase2(texto):
    e = generar_qr_por_etapas(texto)
    print("Matriz con datos + EC insertados (aún SIN máscara):")
    imprimir_matriz(e["matriz_fase2"], base=e["base"], margen=1)

# ---------------------------- FASE 3 ----------------------------------
def mostrar_fase3(texto):
    e = generar_qr_por_etapas(texto)
    base, antes, mask_id = e["base"], e["matriz_fase2"], e["mask_id"]
    despues = e["solo_mascara"]
    tam = len(base)

    print("Fórmulas y penalización de cada máscara (gana la menor):")
    for i in range(8):
        marca = "  <-- ELEGIDA" if i == mask_id else ""
        print(f"  Máscara {i}: {MASK_FORMULAS[i]:<42} penalización = {e['puntajes'][i]}{marca}")

    alterados = verificar_modulos_funcionales(antes, despues, base)
    cambiados = sum(1 for r in range(tam) for c in range(tam)
                    if es_celda_dato(base, r, c) and antes[r][c] != despues[r][c])
    total_datos = sum(1 for r in range(tam) for c in range(tam) if es_celda_dato(base, r, c))
    print(f"\nMáscara aplicada: {mask_id}")

    print("\nANTES de la máscara (▓▓/░░ = datos):")
    imprimir_matriz(antes, base=base, margen=1)

    print("\nMódulos que la máscara invirtió (XX = invertido):")
    for r in range(tam):
        linea = ""
        for c in range(tam):
            if es_celda_dato(base, r, c):
                linea += "XX" if antes[r][c] != despues[r][c] else "· "
            else:
                linea += "██" if base[r][c] == 1 else "  "
        print(linea)

    print("\nDESPUÉS de la máscara + bits de formato (matriz FINAL):")
    imprimir_matriz(e["matriz_final"], margen=1)


# ------------------------- QR FINAL ESCANEABLE -------------------------
def simular_matriz_qr(texto):
    e = generar_qr_por_etapas(texto)
    print(f"\nTexto: '{texto}' | Máscara: {e['mask_id']} | Nivel EC: {EC_LEVEL}\n")
    imprimir_matriz(e["matriz_final"])
    return e["matriz_final"]


# =====================================================================
#  MENÚ
# =====================================================================
def _texto_apto(texto):
    if not validar_caracteres_qr(texto):
        print("\nEl texto no es válido para la norma QR. Cámbialo con la opción 1.")
        return False
    if len(texto) > MAX_CARACTERES:
        print(f"\n⚠ El texto es muy largo para la versión {VERSION}-{EC_LEVEL} "
              f"(máx. {MAX_CARACTERES} caracteres). Acórtalo.")
        return False
    return True


def menu_terminal():
    texto = "QR-2026"

    while True:
        print("\n" + "=" * 42)
        print("    MENÚ DE VALIDACIÓN Y CONVERSIÓN QR")
        print("=" * 42)
        print(f"Texto actual seleccionado: '{texto}'")
        print("-" * 42)
        print("1. Cambiar texto de entrada")
        print("2. Validar texto (Norma Alfanumérica QR)")
        print("3. Convertir texto a vectores (DEC, HEX, BIN)")
        print("4. Ejecutar validación y conversión completas")
        print("5. Datos en zigzag (antes de Reed-Solomon)")
        print("6. Reed-Solomon")
        print("7. Enmascaramiento (antes / después)")
        print("8. QR final")
        print("9. Salir")
        print("=" * 42)

        opcion = input("Selecciona una opción (1-9): ").strip()

        if opcion == "1":
            texto = input("\nIngresa el nuevo texto a evaluar: ")
            print(f">> Texto actualizado a: '{texto}'")

        elif opcion == "2":
            es_valido = validar_caracteres_qr(texto)
            estado = "PERMITIDO " if es_valido else "NO PERMITIDO "
            print(f"\n[RESULTADO VALIDACIÓN]")
            print(f"Texto: '{texto}'")
            print(f"Estatus: {estado}")

        elif opcion == "3":
            resultado = convertidor_Caracter(texto)
            print(f"\n[RESULTADO CONVERSIÓN: '{texto}']")
            print(f"Vector Decimal (DEC)    : {resultado['DEC']}")
            print(f"Vector Hexadecimal (HEX): {resultado['HEX']}")
            print(f"Vector Binario (BIN)    : {resultado['BIN']}")
            print(f"Cadena Binaria Unida    : {resultado['CADENA_BIN']}")

        elif opcion == "4":
            print(f"\n[EVALUACIÓN INTEGRAL PARA: '{texto}']")
            if validar_caracteres_qr(texto):
                print("Estatus: PERMITIDO ")
                res = convertidor_Caracter(texto)
                print(f"DEC: {res['DEC']}")
                print(f"HEX: {res['HEX']}")
                print(f"BIN: {res['BIN']}")
                print(f"Cadena Unida: {res['CADENA_BIN']}")
            else:
                print("Estatus: NO PERMITIDO ")
                print("El texto incluye caracteres no compatibles con el diccionario.")

        elif opcion == "5":
            if _texto_apto(texto):
                mostrar_fase1(texto)

        elif opcion == "6":
            if _texto_apto(texto):
                mostrar_fase2(texto)

        elif opcion == "7":
            if _texto_apto(texto):
                mostrar_fase3(texto)

        elif opcion == "8":
            if _texto_apto(texto):
                simular_matriz_qr(texto)

        elif opcion == "9":
            print("\nSaliendo del programa...")
            break
        else:
            print("\n⚠ Opción no válida. Ingresa un número del 1 al 9.")


#CAMBIOS DE FERNANDO
#Convertidor de Strings a ASCII
def conseguir_valor_ascii(texto: str):
    ascii_array = [ord(char) for char in texto] #Guardar los valores ASCII en un array

    return (ascii_array)

#Convertidor de string a su valor en binario
def conseguir_valor_bin(texto: str):

    #Esta manera es mas directa y asegura convertir los caracteres en su version en binario
    #De manera que si juntas el array en binario entero te da el texto original
    binary_array =  [format(ord(char), "08b") for char in texto]
    return binary_array

if __name__ == "__main__":
    menu_terminal()