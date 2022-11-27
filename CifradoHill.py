import numpy as np
from sympy import Matrix


alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z', '_']


def getInt(mensaje):
    try:
        numero = (input(mensaje))
        if numero.isdigit():
            return int(numero)
        else:
            print("Ingrese solo números")
            return getInt(mensaje)
    except ValueError or TypeError:
        print("Ingrese un valor numérico válido")
        return getInt(mensaje)


def getWord(mensaje):
    try:
        palabra = input(mensaje).lower()
        tamPalabra = len(palabra)
        if tamPalabra != 0 and palabra != " ":
            for elemento in palabra:
                if elemento not in alfabeto:
                    print(
                        "Ingrese solo letras válidas en el alfabeto definido, si quieres usar un espacio utiliza '_' ")
                    return getWord(mensaje)

            return palabra
        else:
            getWord(mensaje)
    except ValueError or TypeError:
        print("Ingrese solo letras válidas en el alfabeto definido, si quieres usar un espacio utiliza '_' ")
        return getWord(mensaje)


def defMatriz(palabra):
    longitud = len(palabra)
    numero = getInt("Ingrese un número para crear la matriz (elementos por columna)>>>")
    if numero <= longitud and numero > 0:
        return numero
    else:
        return defMatriz(palabra)


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


def tamañoClave(palabra, numeroPorFilas):
    try:
        clave = getWord("Ingrese la clave para cifrar o descifrar el mensaje>>>")
        tamanoMaximo = numeroPorFilas * numeroPorFilas
        tamClave = 0
        tamClave = len(clave)
        if tamClave == tamanoMaximo and tamClave > 0:
            return clave
        else:
            print("La clave tiene que ser máximo de ", tamanoMaximo, " y mínimo de ", tamanoMaximo, " caracteres.")
            return tamañoClave(palabra, numeroPorFilas)
    except TypeError:
        print("La clave tiene que ser máximo de ", tamanoMaximo, " y mínimo de ", tamanoMaximo,
              " caracteres, ingrese un valor válido.")
        return tamañoClave(palabra, numeroPorFilas)


def divisoresMod():
    divisoresModulo = []
    for i in range(2, len(alfabeto)):
        if len(alfabeto) % i == 0:
            divisoresModulo.append(i)

    return divisoresModulo


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
    matrizClave = [posicionesClave[numeroPorFilas * i: numeroPorFilas * (i + 1)] for i in range(numeroPorFilas)]
    trasMatrizClave = np.transpose(matrizClave)

    # Comprobar si la clave funciona para encriptar (Determinante != 0 and no divisores en común con el modulo[3,9,27])
    determinanteClave = (np.linalg.det(trasMatrizClave)) // 1
    print("Determinante: ", determinanteClave)

    if not esInversaMod(trasMatrizClave):
        return comprobarClave(palabra, numeroPorFilas, alfabeto)

    divisores = []
    numEsta = False
    for i in range(1, len(alfabeto)):
        if determinanteClave % i == 0:
            divisores.append(i)

    divisoresModulo = divisoresMod()
    for element in divisores:
        if element in divisoresModulo:
            numEsta = True

    if determinanteClave != 0 and numEsta != True:
        return trasMatrizClave
    else:
        print("La clave ingresada no es válida para cifrar, ya que determinante = 0 o tiene divisores en común, "
              "ingrese otra")
        return comprobarClave(palabra, numeroPorFilas, alfabeto)


def esInversaMod(matrizClave):
    try:
        verdad = True
        inversaClave = Matrix(matrizClave).inv_mod(len(alfabeto))
        return verdad
    except ValueError or TypeError:
        print("La matriz no es invertible en módulo ", len(alfabeto))
        verdad = False
        return verdad


def cifradoHill():
    print(">>>>>>>>>>>>>>>>>>>>>>Cifrado<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    # Palabra a cifrar
    palabra = getWord("Ingrese la palabra que quiere cifrar>>>")
    posiciones = []

    # Guardar la posición de cada carácter de la palabra
    if palabra is not None:
        for elemento in palabra:
            if elemento in alfabeto:
                posi = alfabeto.index(elemento)
                posiciones.append(posi)
    else:
        print("Tiene que ingresar alguna palabra para cifrar")
        return cifradoHill()

    # Definir una matriz que represente el mensaje | filas = numeroParaMatriz
    numeroPorFilas = defMatriz(palabra)

    # proceso de clave
    matrizClave = comprobarClave(palabra, numeroPorFilas, alfabeto)
    comprobar = esInversaMod(matrizClave)

    # calculo de columnas
    columnas = calculoColumnas(numeroPorFilas, palabra)

    # completando posiciones con espacios, para llenar la matriz
    posicionesCompletas = completarMatriz(numeroPorFilas, columnas, posiciones, palabra)
    print("----------------------- Mensaje codificado a números -----------------------")
    print(posicionesCompletas)
    print("----------------------------------------------------------------------------")

    # llenando matriz del mensaje
    matrizMensaje = [posicionesCompletas[numeroPorFilas * i: numeroPorFilas * (i + 1)] for i in range(columnas)]
    trasMatrizMensaje = np.transpose(matrizMensaje)
    print("---------------------- Matriz resultante del mensaje -----------------------")
    print(trasMatrizMensaje)
    print("----------------------------------------------------------------------------")

    print("----------------------- Matriz resultante de la clave ----------------------")
    print(matrizClave)
    print("----------------------------------------------------------------------------")

    # multiplicar matrices
    matrizResultado = np.dot(matrizClave, trasMatrizMensaje)
    print("------ Matriz resultado de la multiplicación del mensaje con la clave ------")
    print(matrizResultado)
    print("----------------------------------------------------------------------------")

    # aplicar modulo a la matriz resultado
    matrizResultado = matrizResultado % len(alfabeto)
    print("--------------------- Matriz resultado aplicando mod 27 --------------------")
    print(matrizResultado)
    print("----------------------------------------------------------------------------")

    # convertir matriz a array
    matrizEnInt = matrizResultado.astype(int)
    listaResultado = matrizEnInt.flatten(order='F')
    print("----------------- Mensaje cifrado y codificado en números ------------------")
    print(listaResultado)
    print("----------------------------------------------------------------------------")

    # obtener mensaje cifrado
    respuesta = []
    for elemento in listaResultado:
        letra = alfabeto[elemento]
        if letra in alfabeto:
            respuesta.append(letra)

    print("----------------------------------------------------------------------------")
    print("El mensaje cifrado es: ", ''.join(respuesta))
    print("----------------------------------------------------------------------------")


def descifradoHill():
    print(">>>>>>>>>>>>>>>>>>>>>>Descifrado<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    # Palabra a cifrar
    palabra = getWord("Ingrese la palabra que quiere descifrar>>>")
    posiciones = []

    # Guardar la posición de cada carácter de la palabra
    if palabra is not None:
        for elemento in palabra:
            if elemento in alfabeto:
                posi = alfabeto.index(elemento)
                posiciones.append(posi)
    else:
        print("Tiene que ingresar alguna palabra para descifrar")
        return descifradoHill()

    # Definir una matriz que represente el mensaje | filas = numeroParaMatriz
    numeroPorFilas = defMatriz(palabra)

    # calculo de columnas
    columnas = calculoColumnas(numeroPorFilas, palabra)

    # completando posiciones con espacios, para llenar la matriz
    posicionesCompletas = completarMatriz(numeroPorFilas, columnas, posiciones, palabra)

    # proceso de clave
    matrizClave = comprobarClave(palabra, numeroPorFilas, alfabeto)
    print("--------------------- Criptotexto codificado a números ---------------------")
    print(posicionesCompletas)
    print("----------------------------------------------------------------------------")
    print("----------------------- Matriz resultante de la clave ----------------------")
    print(matrizClave)
    print("----------------------------------------------------------------------------")

    # llenando matriz del mensaje
    matrizMensaje = [posicionesCompletas[numeroPorFilas * i: numeroPorFilas * (i + 1)] for i in range(columnas)]
    trasMatrizMensaje = np.transpose(matrizMensaje)
    print("-------------------- Matriz resultante del criptotexto ---------------------")
    print(trasMatrizMensaje)
    print("----------------------------------------------------------------------------")

    inversaClave = Matrix(matrizClave).inv_mod(len(alfabeto))
    print("---------------------- Matriz invertida de la clave ------------------------")
    print(inversaClave)
    print("----------------------------------------------------------------------------")

    resultadoTemp = np.dot(inversaClave, trasMatrizMensaje)
    print("---- Matriz resultado de la multiplicación del criptotexto con la clave ----")
    print(resultadoTemp)
    print("----------------------------------------------------------------------------")
    resultadoTemp = resultadoTemp % len(alfabeto)
    print("--------------------- Matriz resultado aplicando mod 27 --------------------")
    print(resultadoTemp)
    print("----------------------------------------------------------------------------")

    matrizEnInt1 = resultadoTemp.astype(int)
    listaResultado1 = matrizEnInt1.flatten(order='F')
    print("---------------- Mensaje descifrado y codificado en números ----------------")
    print(listaResultado1)
    print("----------------------------------------------------------------------------")

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
                         "3. Realizar solo descifrado. \n "
                         "4. Salir del programa. \n "))

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
                             "3. Realizar solo descifrado. \n "
                             "4. Salir del programa. \n "))
    except ValueError or TypeError as ve:
        print("Ingrese valores válidos, por favor", ve)
        return start()


start()