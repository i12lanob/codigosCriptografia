import re
import math
import random

###################################################################
#Funciones útiles                                                 #
###################################################################
#Función obtener_numero_entero, para comprobar que solo se introducen números
def obtener_numero_entero(mensaje):
    while True:
        entrada = input(mensaje)
        if entrada.isdigit():
            return int(entrada)
        else:
            print("Por favor, introduce solo dígitos.")

#Función generarMatriz, rellena una matriz con números aleatorios. 
def generarMatriz(num):
    matriz = []
    for f in range(num):
        fila = []
        for c in range(num):
            fila.append(random.randint(1, 10))  # Genera un número aleatorio entre 1 y 10
        matriz.append(fila)

    print(matriz) # Visualizar matriz generada 
    return matriz

#Función calculoDeterminante
def calculoDeterminante(A): 

    # Matriz de 1x1
    if len(A) == 1: 
        return A[0][0]

    # Matriz de 2x2
    if len(A) == 2: 
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    
    # Matriz mayor que 2x2
    det = 0
    for col in range(len(A)):
        # Crear la submatriz sin la primera fila y sin la columna col
        submatriz = []
        for fila in range(1, len(A)):
            nueva_fila = []
            for columna in range(len(A[fila])):
                if columna != col: 
                    nueva_fila.append(A[fila][columna])
            submatriz.append(nueva_fila)
        
        # Signo: 1 si la columna es par, -1 si es impar
        signo = 1 if col % 2 == 0 else -1
         
        det += signo * A[0][col] * calculoDeterminante(submatriz) # Sumar el producto del signo, el elemento y el determinante de la submatriz

    return det

#Función comprobarCalculoInversa. Comprobar si se puede calcular la inversa modular de una matriz. 
def comprobarCalculoInversa(n, det): 
    if algeucl(n, det)==1: 
        return 1
    else:  
        print("El determinante y", n, "no son coprimos, no se puede calcular la inversa")

#Función matrizTraspuesta
def matrizTraspuesta(A):

    submatriz = []
    for col in range(len(A)): 
        nueva_fila = []
        for fil in range(len(A)): 
            nueva_fila.append(A[fil][col]) # Intercambiar las filas por columnas

        submatriz.append(nueva_fila)

    return submatriz

#Función matrizAdjunta. 
def matrizAdjunta(A): 

    adjunta = []
    for fil in range(len(A)): # Empezar por la primera fila y primera columna
        fila_adjunta = []
        for col in range(len(A)):
            submatriz = [] 
            for f in range (len(A)):
                if f != fil:
                    nueva_fila = []
                    for c in range(len(A[f])):
                        if c != col: # Crear una matriz con los elementos que no están en la fila fil y columna col 
                            nueva_fila.append(A[f][c]) 
                    
                    submatriz.append(nueva_fila) # Introducir en la submatriz 

            # Calcular el signo alternante para la adjunta
            signo = 1 if (fil + col)%2 == 0 else -1
            
            # Calcular el valor del cofactor teniendo en cuenta el signo y el determinante
            cofactor = signo * calculoDeterminante(submatriz) 

            # Añadir el cofactor a la fila adjunta
            fila_adjunta.append(cofactor)
        
        # Añadir la fila adjunta a la matriz de adjunta
        adjunta.append(fila_adjunta)

    return adjunta

#Función calcularModulo. 
def calcularModulo(texto_cifrado, n):

    texto_modulo = []

    for i in range(len(texto_cifrado)):
        texto_modulo.append(texto_cifrado[i]%n)

    return texto_modulo

#Función NumberToText. Convertir número a carácter.  
def NumberToText(texto):
    cadena_texto = []

    for num in texto:
            numero = chr(num + ord('A')) # Convertir a un número en Z26 (A=0, ..., Z=25)
            cadena_texto.append(numero)
    
    return cadena_texto

###################################################################
#Funciones principales                                            #
###################################################################

########################### Ejercicio 1 ###########################
#Función algeucl. Calcula el MCD de a y b usando el Algoritmo de Euclides.
def algeucl(a,b): 
    while(b!=0) :
        temp=b # Crear una variable temporal para guardar b
        b=a%b # Actualizar b con el resto de a y b (nuevo divisor)
        a=temp # Actualizar a (nuevo dividendo)
    return a
 
#Función invmod
def invmod(p, n):
    if p >= 0 and n > 0:
        if algeucl(p, n) == 1:
            # Algoritmo extendido de Euclides
            a, b = n, p
            x0, x1 = 0, 1
            while b > 1:
                q = a // b
                a, b = b, a - q * b
                x0, x1 = x1, x0 - q * x1
            if x1 < 0:
                x1 += n
            return x1
        else:
            return "Los números no son coprimos, no se puede calcular el inverso."
    else:
        return "Los números deben ser naturales."

#Función eulerfun. Devuelve una lista con todos los elementos invertibles en Zn.
def eulerfun(n): 
    invertibles = []
    for a in range (1, n): # Para que sea invertible tiene que tener el mcd==1
        if algeucl (n, a) == 1: 
            invertibles.append(a) # Si es 1 lo guardar en un vector 
    return invertibles

#Función InvModMatrix. Calcula la inversa de una matriz en el módulo n si existe.
def InvModMatrix(A, n):

    # Calcular determinante de la matriz A
    det = calculoDeterminante(A)
    
    # Si el mcd==1 del determinante y de n entonces se puede calcular la inversa modular
    if comprobarCalculoInversa(n, det) == 1:

        det = det % n # Si el determinante es negativo nos aseguramos que está dentro del módulo

        det_inv = invmod(det, n) # Calcular determinante inverso

        traspuesta = matrizTraspuesta(A) 

        adjunta = matrizAdjunta(traspuesta)

        # Una vez obtenida la matriz adjunta se calcula la inversa modular
        inversa_modular = []
        for fila in adjunta:
            fila_inversa = []
            for elem in fila:
                fila_inversa.append((det_inv * elem) % n)
            inversa_modular.append(fila_inversa)

        print("La inversa modular de la matriz en módulo", n, "es:")
        for fila in inversa_modular:
            print(fila)
        return inversa_modular

########################### Ejercicio 2 ###########################
# Función TextToNumber. Convierte una cadena de texto a una cadena numérica en Z26, eliminando espacios y caracteres especiales.
def TextToNumber(texto):
    
    texto = texto.upper()  # Convertir el texto a mayúsculas para facilitar el mapeo
    cadena_numerica = []
    
    for char in texto:
        if 'A' <= char <= 'Z':  # Solo considerar letras
            numero = ord(char) - ord('A')  # Convertir a un número en Z26 (A=0, ..., Z=25)
            cadena_numerica.append(numero)
    
    return cadena_numerica

########################### Ejercicio 3 ###########################
# Función afinCypher. Realiza el cifrado afín en el texto ingresado usando los valores k y d, donde f(x) = kx + d.
def afinCypher(texto, k, d):
    # Validar que k y 26 sean coprimos
    if algeucl(k, 26) != 1:
        return "El valor de k no es coprimo con 26, elige otro valor para k."
    
    # Convertir el texto en números usando TextToNumber
    numeros = TextToNumber(texto)
    
    # Aplicar el cifrado afín: f(x) = (k * x + d) % 26
    cifrado = [(k * x + d) % 26 for x in numeros]
    
    # Convertir los números cifrados de vuelta a letras
    texto_cifrado = ''.join(chr(num + ord('A')) for num in cifrado) # chr convierte en su carácter
    
    return texto_cifrado

########################### Ejercicio 4 ###########################
#Función encriptarCifradoHill. Encriptar un mensaje con cifrado Hill. 
def encriptarCifradoHill(texto, matriz): 
    n = 26 # Módulo 26. A=0, B=1, ..., Z=25. 
    det = calculoDeterminante(matriz) # Calcular determinante de la matriz. 

    if comprobarCalculoInversa(n, det)==1: # Comprobar si se puede calcular la inversa modular, si no se puede calcular no se podrá desencriptar. 
        vector_texto = []
        texto_cifrado = []

        vector_texto = TextToNumber(texto)

        for fila in range(len(matriz)): # Recorrer fila a fila la matriz. 
            f = 0 
            aux = 0 # Utilizada para guardar el valor de la multiplicación fila*columna
            for colum in range(len(matriz)): # Recorrer columna a columna la matriz. 
                aux += matriz[fila][colum] * vector_texto[f] # Calcular multiplicación de fila*columna
                f += 1
                
            texto_cifrado.append(aux)

        texto_cifrado = calcularModulo(texto_cifrado, n) 

        return texto_cifrado
    
    else: 
        return -1

#Función desencriptarCifradoHill. Desencriptar un mensaje con cifrado Hill. 
def desencriptarCifradoHill(mensajeEncriptado, matriz):
    n = 26 # Módulo 26
    matriz_inversa = InvModMatrix(matriz, n) # Calcular la inversa modular la matriz. 

    texto_descifrado = []

    for fila in range(len(matriz)): # Recorrer fila a fila la matriz. 
        f = 0
        aux = 0 # Utilizada para guardar el valor de la multiplicación fila*columna
        for colum in range(len(matriz_inversa)): # Recorrer columna a columna la matriz. 
            aux += matriz_inversa[fila][colum] * mensajeEncriptado[f] # Calcular multiplicación de fila*columna
            f += 1
                
        texto_descifrado.append(aux)

    texto_descifrado = calcularModulo(texto_descifrado, n) 

    return texto_descifrado    

############################## Menú ###############################
#Aqui inicia el programa, primero pido que elija una opcion
print("1. Algoritmo de euclides")
print("2. Inversos")
print("3. Elementos invertibles")
print("4. Inversa modular matriz")
print("5. Caracteres a cadena numerica Z26")
print("6. Programa cifrado afin")
print("7. Cifrado Hill")
op=input("Elige una de las opciones: ")

op=int(op)
if op==1: 
    a = 18
    b = 5
    #a = obtener_numero_entero("Introduce el valor de a: ")
    #b = obtener_numero_entero("Introduce el valor de b: ")
    print("El algoritmo de euclides con los numeros ", a, " y ", b, " es: ", algeucl(a, b))

if op==2: 
    a = 5
    b = 18
    #a = obtener_numero_entero("Introduce el valor de a: ")
    #b = obtener_numero_entero("Introduce el valor de b: ")
    print("El algoritmo de euclides con los numeros ", a, " y ", b, " es: ", invmod(a, b))

if op==3: 
    n = 8
    #n = obtener_numero_entero("Introduce el valor de n: ")
    invertibles = []
    invertibles = eulerfun(n)
    print("Los invertibles son:", invertibles); 

if op==4:
    n = 4
    dimension=3 # Dimensión de la matriz
    #n = obtener_numero_entero("Introduce el valor de n: ")
    #dimension = obtener_numero_entero("Introduce el valor de la dimension de la matriz: ")

    A = generarMatriz(dimension) # Generar una matriz de 3x3
    InvModMatrix(A, n)

if op==5:
    texto = input("Introduce el texto llano para cifrar con el cifrado afín: ")
    print(f"El texto cifrado usando el cifrado afín es: {TextToNumber(texto)}")

if op==6:
    texto = input("Introduce el texto llano para cifrar con el cifrado afín: ")
    k = obtener_numero_entero("Introduce el valor de k (debe ser coprimo con 26): ")
    d = obtener_numero_entero("Introduce el valor de d: ")

    print(f"El texto cifrado usando el cifrado afín es: {afinCypher(texto, k, d)}")

if op==7: 
    texto = input("Introduce el texto llano para cifrar con el cifrado Hill: ")
    #dimension = obtener_numero_entero("Introduce el valor de la dimension de la matriz: ")
    dimension=3
    #matriz = generarMatriz(dimension)
    matriz = [ [ 6, 24, 1 ], [ 13, 16, 10 ], [ 20, 17, 15 ] ]
    encriptado=encriptarCifradoHill(texto, matriz)

    if encriptado != -1:
        print("El texto en cifrado Hill es: ", encriptado)

    
        desencriptado=desencriptarCifradoHill(encriptado, matriz)
        print("El texto en descifrado Hill es: ", desencriptado)
        print("Significado del mensaje desencriptado: ", NumberToText(desencriptado))
    else : 
        print("No se puede cifrar.")