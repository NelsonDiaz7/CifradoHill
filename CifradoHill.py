import numpy as np


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
    columnas = int(tamaño / numeroPorFilas)
    if tamaño % numeroPorFilas != 0:
        columnas = columnas + 1
        return columnas
    else:
        return columnas


def completarMatriz(numeroPorFilas, columnas, posiciones, palabra):
    longitudPalabra = len(palabra)
    totalCaracteres = numeroPorFilas * columnas
    cantidadAñadir = totalCaracteres - longitudPalabra
    if cantidadAñadir > 0:
        for i in range(cantidadAñadir):
            posiciones.append(26)

        return posiciones
    else:
        return posiciones


def completarMatrizClave(numeroPorFilas, posicionesClave, clave):
    longitudClave = len(clave)
    totalCaracteres = numeroPorFilas * numeroPorFilas
    cantidadAñadir = totalCaracteres - longitudClave
    if cantidadAñadir > 0:
        for i in range(cantidadAñadir):
            posicionesClave.append(26)

        return posicionesClave
    else:
        return posicionesClave


def tamañoClave(palabra):
    clave = getWord("Ingrese la clave para cifrar el mensaje>>>")
    tamClave = len(clave)
    tamPalabra = len(palabra)
    # if tamClave <= tamPalabra:
    return clave
    # else:
    #    print("La clave tiene que ser del mismo tamaño que la palabra a cifrar o más pequeña")
    #    return tamañoClave(palabra)


def comprobarClave(palabra, numeroPorFilas, alfabeto):
    # Pedir clave para cifrar
    clave = tamañoClave(palabra)
    posicionesClave = []

    # Guardar la posición de cada carácter de la clave
    for elemento in clave:
        if elemento in alfabeto:
            posi = alfabeto.index(elemento)
            posicionesClave.append(posi)

    print("", posicionesClave)
    print(" ")

    # Llenando matriz de la clave
    posicionesCompletaClave = completarMatrizClave(numeroPorFilas, posicionesClave, clave)
    matrizClave = [posicionesCompletaClave[numeroPorFilas * i: numeroPorFilas * (i + 1)] for i in range(numeroPorFilas)]
    trasMatrizClave = np.transpose(matrizClave)
    print(trasMatrizClave)

    # Comprobar si la clave funciona para encriptar (Determinante != 0 and no tener divisores en común con el modulo[1,3,9,27])
    determinanteClave = int(np.linalg.det(trasMatrizClave))
    print("Determinante: ", determinanteClave)

    divisores = []
    numEsta = False
    for i in range(1, 27):
        if determinanteClave % i == 0:
            divisores.append(i)

    print("Divisores del determinante: ", divisores)
    divisoresModulo = [3, 9, 27]
    for element in divisores:
        if element in divisoresModulo:
            numEsta = True

    print("¿El número está en los divisores?", numEsta)

    if determinanteClave != 0 and numEsta != True:
        print("La clave ingresada es valida para cifrar")
        return trasMatrizClave
    else:
        print("La clave ingresada no es valida para cifrar, ingrese otra")
        return comprobarClave(palabra, numeroPorFilas, alfabeto)


def cifradoHill():
    # Definir alfabeto (En este caso minisculas)
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

    # Definir una matriz que represente el mensaje | filas = numeroParaMatriz
    numeroPorFilas = defMatriz(palabra)

    # calculo de columnas
    columnas = calculoColumnas(numeroPorFilas, palabra)

    # completando posiciones con espacios, para llenar la matriz
    posicionesCompletas = completarMatriz(numeroPorFilas, columnas, posiciones, palabra)

    # llenando matriz del mensaje
    matrizMensaje = [posicionesCompletas[numeroPorFilas * i: numeroPorFilas * (i + 1)] for i in range(columnas)]
    trasMatrizMensaje = np.transpose(matrizMensaje)
    print(trasMatrizMensaje)
    print("-----------------------------")

    # proceso de clave
    matrizClave = comprobarClave(palabra, numeroPorFilas, alfabeto)
    matrizClaveInversa = np.linalg.inv(matrizClave)
    print(matrizClaveInversa)
    print("-----------------------------")

    # multiplicar matrices
    matrizResultado = np.dot(matrizClaveInversa, trasMatrizMensaje)
    print(matrizResultado)
    print("-----------------------------")

    # aplicar modulo a la matriz resultado
    matrizResultado = matrizResultado % 27
    print(matrizResultado)
    print("-----------------------------")

    # convertir matriz a array
    matrizEnInt = matrizResultado.astype(int)
    listaResultado = matrizEnInt.flatten(order='F')
    print(listaResultado)
    print("-----------------------------")

    # obtener mensaje cifrado
    respuesta = []
    for elemento in listaResultado:
        letra = alfabeto[elemento]
        if letra in alfabeto:
            respuesta.append(letra)

    print("mensaje cifrado: ", respuesta)
    print("mensaje cifrado: ", ' '.join(respuesta))


cifradoHill()
