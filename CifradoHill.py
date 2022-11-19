import numpy as np
import random


def getInt(mensaje):
    try:
        numero = (input(mensaje))
        if numero.isdigit():
            return int(numero)
        else:
            print("Ingrese solo números")
            return getInt(mensaje)
    except ValueError or TypeError:
        print("ingrese un valor númerico valido")
        return getInt(mensaje)


def getWord(mensaje):
        alfabeto = inicilizarAlfabeto()
        palabra = input(mensaje).lower()
        for elemento in palabra:
            if elemento not in alfabeto:
                print("Ingrese solo letras validas en el alfabeto definido")
                return getWord(mensaje)

        return palabra


def defMatriz(palabra):
    longitud = len(palabra)
    numero = getInt("Ingrese un número para crear la matriz (elementos por columna)>>>")
    if numero <= longitud:
        return numero
    else:
        return defMatriz(palabra)


def inicilizarAlfabeto():
    alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z', ' ']
    return alfabeto


def calculoColumnas(numeroPorFilas, palabra):
    tamaño = len(palabra)
    columnas = 0
    if tamaño % numeroPorFilas != 0:
        columnas = int(tamaño / numeroPorFilas)
        columnas = columnas + 1
        return columnas
    else:
        return columnas


def cifradoHill():
    # Definir alfabeto (En minisculas)
    alfabeto = inicilizarAlfabeto()

    # Palabra a cifrar
    palabra = getWord("Ingrese la palabra que quiere cifrar>>>")
    posiciones = []

    # Guardar la posición de cada carácter de la palabra
    for elemento in palabra:
        if elemento in alfabeto:
            posi = alfabeto.index(elemento)
            posiciones.append(posi)

    print("", posiciones)
    tamañoPosic = len(posiciones)

    # Definir una matriz que represente el mensaje
    # filas = numeroParaMatriz
    numeroPorFilas = defMatriz(palabra)

    # calculo de columnas
    columnas = calculoColumnas(numeroPorFilas, palabra)

    matriz = []
    for i in range(columnas):
        matriz.append([])
        for j in range(numeroPorFilas):
            for z in posiciones:
                matriz[i].append(z)

    print(matriz)

    # llenando matriz A
    # matrizA = [posiciones[numeroPorFilas * i: numeroPorFilas * (i + 1)] for i in range(columnas)]
    # trasMatrizA = np.transpose(matrizA)
    # print(trasMatrizA)

    # matriz identidad
    # matrizIdentidad = np.identity(numeroParaMatriz)
    # print("Matriz identidad", matrizIdentidad)

    # obteniendo matriz invertible
    # matrizInvertible = matrizIdentidad/matrizA
    # print("Matriz invetible", matrizInvertible)

    # Multiplicar matriz invertible por matriz A = Aprima
    # aPrima = np.dot(matrizInvertible*matrizA)
    # print("Matriz Aprima", aPrima)

    # Obteniendo matriz invertible de matriz A
    # matrizInvertible = np.linalg.inv(matrizA)
    # matrizInvertible = trasMatrizA ** -1
    # print("Matriz invetible", matrizInvertible)

    # Multiplicar matriz invertible por matriz A = Aprima
    # aPrima = np.dot(matrizInvertible, trasMatrizA)
    # print("Matriz Aprima", aPrima)

    # Aplicar modulo 27 a la matriz A prima
    # matrizResultado = aPrima % 27
    # print("Matriz resultado", matrizResultado)

    # Mensaje cifrado
    # listaResultado = matrizResultado.tolist()
    # print("Mensaje cifrado: ", listaResultado)


cifradoHill()
