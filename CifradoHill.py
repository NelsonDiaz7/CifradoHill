import numpy as np
from sympy import Matrix


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
    tamPalabra = len(palabra)
    if tamPalabra != 0:
        for elemento in palabra:
            if elemento not in alfabeto:
                print("Ingrese solo letras válidas en el alfabeto definido, si quieres usar un espacio utiliza '_' ")
                return getWord(mensaje)

        return palabra
    else:
        getWord(mensaje)


def defMatriz(palabra):
    longitud = len(palabra)
    numero = getInt("Ingrese un número para crear la matriz (elementos por columna)>>>")
    if numero <= longitud and numero > 0:
        return numero
    else:
        return defMatriz(palabra)


def inicilizarAlfabeto():
    alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z', '_']
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


def tamañoClave(palabra, numeroPorFilas):
    try:
        clave = getWord("Ingrese la clave para cifrar o descifrar el mensaje>>>")
        tamanoMaximo = numeroPorFilas * numeroPorFilas
        tamClave = 0
        tamClave = len(clave)
        if tamClave == tamanoMaximo and tamClave > 0:
            return clave
        else:
            print("La clave tiene que ser maximo de ", tamanoMaximo, " y mínimo de ", tamanoMaximo, " caracteres.")
            return tamañoClave(palabra, numeroPorFilas)
    except TypeError:
        print("La clave tiene que ser máximo de ", tamanoMaximo, " y mínimo de ", tamanoMaximo," caracteres, ingrese un valor valido.")
        return tamañoClave(palabra, numeroPorFilas)


def comprobarClave(palabra, numeroPorFilas, alfabeto):
    # Pedir clave para cifrar
    clave = tamañoClave(palabra, numeroPorFilas)
    posicionesClave = []

    # Guardar la posición de cada carácter de la clave
    for elemento in clave:
        if elemento in alfabeto:
            posi = alfabeto.index(elemento)
            posicionesClave.append(posi)

    # Llenando matriz de la clave
    posicionesCompletaClave = completarMatrizClave(numeroPorFilas, posicionesClave, clave)
    matrizClave = [posicionesCompletaClave[numeroPorFilas * i: numeroPorFilas * (i + 1)] for i in range(numeroPorFilas)]
    trasMatrizClave = np.transpose(matrizClave)

    # Comprobar si la clave funciona para encriptar (Determinante != 0 and no divisores en común con el modulo[3,9,27])
    determinanteClave = (np.linalg.det(trasMatrizClave)) // 1

    divisores = []
    numEsta = False
    for i in range(1, 27):
        if determinanteClave % i == 0:
            divisores.append(i)

    # print("Divisores del determinante: ", divisores)
    divisoresModulo = [3, 9, 27]
    for element in divisores:
        if element in divisoresModulo:
            numEsta = True

    if determinanteClave != 0 and numEsta != True:
        # print("La clave ingresada es valida para cifrar")
        return trasMatrizClave
    else:
        print("La clave ingresada no es valida para cifrar ya que determinante = 0 o tiene divisores en común, "
              "ingrese otra")
        return comprobarClave(palabra, numeroPorFilas, alfabeto)


def cifradoHill():
    print(">>>>>>>>>>>>>>>>>>>>>>Cifrado<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
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

    # Definir una matriz que represente el mensaje | filas = numeroParaMatriz
    numeroPorFilas = defMatriz(palabra)

    # calculo de columnas
    columnas = calculoColumnas(numeroPorFilas, palabra)

    # completando posiciones con espacios, para llenar la matriz
    posicionesCompletas = completarMatriz(numeroPorFilas, columnas, posiciones, palabra)

    # llenando matriz del mensaje
    matrizMensaje = [posicionesCompletas[numeroPorFilas * i: numeroPorFilas * (i + 1)] for i in range(columnas)]
    trasMatrizMensaje = np.transpose(matrizMensaje)

    # proceso de clave
    matrizClave = comprobarClave(palabra, numeroPorFilas, alfabeto)

    # multiplicar matrices
    matrizResultado = np.dot(matrizClave, trasMatrizMensaje)

    # aplicar modulo a la matriz resultado
    matrizResultado = matrizResultado % 27

    # convertir matriz a array
    matrizEnInt = matrizResultado.astype(int)
    listaResultado = matrizEnInt.flatten(order='F')

    # obtener mensaje cifrado
    respuesta = []
    for elemento in listaResultado:
        letra = alfabeto[elemento]
        if letra in alfabeto:
            respuesta.append(letra)

    print("-----------------------------")
    print("El mensaje cifrado es: ", ''.join(respuesta))
    print("-----------------------------")


def descifradoHill():
    print(">>>>>>>>>>>>>>>>>>>>>>Descifrado<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    # Definir alfabeto (En este caso minisculas)
    alfabeto = inicilizarAlfabeto()

    # Palabra a cifrar
    palabra = getWord("Ingrese la palabra que quiere descifrar>>>")
    posiciones = []

    # Guardar la posición de cada carácter de la palabra
    for elemento in palabra:
        if elemento in alfabeto:
            posi = alfabeto.index(elemento)
            posiciones.append(posi)

    # Definir una matriz que represente el mensaje | filas = numeroParaMatriz
    numeroPorFilas = defMatriz(palabra)

    # proceso de clave
    matrizClave = comprobarClave(palabra, numeroPorFilas, alfabeto)

    # calculo de columnas
    columnas = calculoColumnas(numeroPorFilas, palabra)

    # completando posiciones con espacios, para llenar la matriz
    posicionesCompletas = completarMatriz(numeroPorFilas, columnas, posiciones, palabra)

    # llenando matriz del mensaje
    matrizMensaje = [posicionesCompletas[numeroPorFilas * i: numeroPorFilas * (i + 1)] for i in range(columnas)]
    trasMatrizMensaje = np.transpose(matrizMensaje)

    inversaClave = Matrix(matrizClave).inv_mod(27)

    resultadoTemp = np.dot(inversaClave, trasMatrizMensaje)
    resultadoTemp = resultadoTemp % 27

    matrizEnInt1 = resultadoTemp.astype(int)
    listaResultado1 = matrizEnInt1.flatten(order='F')

    # obtener mensaje descifrado
    respuesta1 = []
    for elemento in listaResultado1:
        letra = alfabeto[elemento]
        if letra in alfabeto:
            respuesta1.append(letra)

    #    print("mensaje descifrado: ", respuesta1)
    print("-----------------------------")
    print("El mensaje descifrado es: ", ''.join(respuesta1))
    print("-----------------------------")


def start():
    try:
        menu = int(input("Menú principal: \n "
                         "1. Realizar cifrado y descifrado. \n "
                         "2. Realizar solo cifrado. \n "
                         "3. Realizar solo descifrado \n "
                         "4. Salir del programa \n "))

        while menu != 4:

            if menu == 1:
                cifradoHill()
                descifradoHill()
            elif menu == 2:
                cifradoHill()
            elif menu == 3:
                descifradoHill()
            else:
                print("Digita un número que sea valido")

            menu = int(input("Menú principal: \n "
                             "1. Realizar cifrado y descifrado. \n "
                             "2. Realizar solo cifrado. \n "
                             "3. Realizar solo descifrado \n "
                             "4. Salir del programa \n "))
    except ValueError or TypeError:
        print("Ingrese valores validos por favor")
        return start()


start()
