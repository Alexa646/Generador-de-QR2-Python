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
        print("5. Salir")
        print("=" * 42)

        opcion = input("Selecciona una opción (1-5): ").strip()

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
            print("\nSaliendo del programa...")
            break
        else:
            print("\n⚠ Opción no válida. Ingresa un número del 1 al 5.")

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
