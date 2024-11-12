###################################################################
#Práctica 2: Cifrado Afín y Cifrado Hill                          #
###################################################################
#Blanca Lara Notario                                              #
#Rafael Bueno Espinosa                                            #
#Francisco Bueno Espinosa                                         #
###################################################################

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

#Función encriptarMensaje. Función general para encriptar mensajes cuando ya tienen la dimensión correcta. 
def encriptarMensaje(vector_texto, matriz, n):
    
    texto_cifrado = []
    for fila in range(len(matriz)): # Recorrer fila a fila la matriz. 
        f = 0 
        aux = 0 # Utilizada para guardar el valor de la multiplicación fila*columna
        for colum in range(len(matriz)): # Recorrer columna a columna la matriz. 
            aux += matriz[fila][colum] * vector_texto[f] # Calcular multiplicación de fila*columna
            f += 1
            
        texto_cifrado.append(aux)

    texto_cifrado = calcularModulo(texto_cifrado, n)

    return texto_cifrado 

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
    n=26
    # Validar que k y 26 sean coprimos
    if algeucl(k, n) != 1:
        return "El valor de k no es coprimo con 26, elige otro valor para k."

    # Convertir el texto en números usando TextToNumber
    numeros = TextToNumber(texto)

    # Aplicar el cifrado afín: f(x) = (k * x + d) % 26
    cifrado = [(k * x + d) % n for x in numeros]

    # Convertir los números cifrados de vuelta a letras
    texto_cifrado = ''.join(chr(num + ord('A')) for num in cifrado) # chr convierte ASCII en su carácter

    return texto_cifrado

# Función afinDecrypher. Realiza el descifrado afín dado el texto cifrado y los valores de k y d.
def afinDecrypher(texto_cifrado, k, d):

    # Validar que k y 26 sean coprimos
    n=26 

    if algeucl(k, n) != 1:
        return "El valor de k no es coprimo con 26, elige otro valor para k."
    
    # Calcular el inverso de k en Z26
    k_inv = invmod(k, n)
    if isinstance(k_inv, str):
        return k_inv  # Si no tiene inverso, retorna el mensaje de error de invmod
    
    # Convertir el texto cifrado en números usando TextToNumber
    numeros = TextToNumber(texto_cifrado)
    
    # Aplicar el descifrado afín: f^-1(y) = k_inv * (y - d) % 26
    descifrado = [(k_inv * (y - d)) % n for y in numeros]
    
    # Convertir los números descifrados de vuelta a letras
    texto_descifrado = ''.join(chr(num + ord('A')) for num in descifrado)
    
    return texto_descifrado
    
# Función guesskd. Estima posibles valores de k y d
def guesskd(identificaciones):

    posibles_kd = []
    letras_z26 = {char: i for i, char in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}  # Mapeo letras -> Z26

    # Obtiene los pares de identificaciones
    identificaciones_llano_cifrado = list(identificaciones.items())

    # Extrae la primera y segunda identificación.
    e1, p1 = identificaciones_llano_cifrado[0]  # Las letras cifradas son e1, e2, y las letras del texto plano son p1, p2
    e2, p2 = identificaciones_llano_cifrado[1]  # Las letras cifradas son e1, e2, y las letras del texto plano son p1, p2

    # Convierte letras a números Z26
    p1_num = letras_z26[p1.upper()] #Devolverán el correspondiente número en Z26.
    e1_num = letras_z26[e1.upper()] #Devolverán el correspondiente número en Z26.
    p2_num = letras_z26[p2.upper()] #Devolverán el correspondiente número en Z26.
    e2_num = letras_z26[e2.upper()] #Devolverán el correspondiente número en Z26.

    # Resuelve el sistema de ecuaciones para obtener k y d
    # e1 = (k * p1 + d) % 26
    # e2 = (k * p2 + d) % 26
    try:
        # Resuelve para k usando la relación (e1 - e2) / (p1 - p2) en mod 26
        delta_e = (e1_num - e2_num) % 26
        delta_p = (p1_num - p2_num) % 26
       
        
        # Busca todos los valores de k y d que satisfacen el sistema
        for k in range(1, 26):  # Buscamos en Z26
            if (k * delta_p) % 26 == delta_e: # Buscamos que satisfaga la ecuación K x Δp≡Δ
                d = (e1_num - k * p1_num) % 26 # Calcula el valor de d
               
                posibles_kd.append((k, d)) # Añadimos el valor de k y d calculados en posibles_kd

    except ZeroDivisionError:
        return "No se puede resolver: los identificadores deben ser diferentes para evitar un sistema indeterminado."
    
    return posibles_kd

#Función afinCriptoanalisis. Utiliza todas las funciones anteriores. 
def afinCriptoanalisis(texto_cifrado):
    print("Iniciando criptoanálisis interactivo del cifrado afín.")
    
    # Solicitar identificaciones de letras
    identificaciones = {} # Diccionario para las letras

    while len(identificaciones) < 2: #  Obtenemos dos pares de la forma p->e
        letra_cifrada = input("Introduce una letra del texto cifrado: ").upper() #Pedimos la letra cifrada
        print("\n")
        letra_llano = input("Introduce la letra correspondiente en el texto llano: ").upper()#  Pedimos la letra del texto llano.
        print("\n")
        identificaciones[letra_cifrada] = letra_llano
    
    # Obtener posibles valores de k y d
    posibles_kl_d = guesskd(identificaciones)    # Llama a guesskd() con los pares de letras para calcular  posibles valores de k y d
    print("Posibles valores de k y d encontrados:")
    
    for kd in posibles_kl_d:
        k, d = kd
        print(f"Probando con k = {k}, d = {d}")
        
        # Intentar descifrar usando los valores de k y d
        texto_descifrado = afinDecrypher(texto_cifrado, k, d)  # Llama a afinDecrypher() para intentar descifrar con k y d actuales
        print(f"Texto descifrado con k = {k}, d = {d}: {texto_descifrado}")
        
        # Confirmación con el usuario
        continuar = input("¿Es este el texto llano correcto? (s/n): ")
        
        if continuar.lower() == 's':
            return texto_descifrado
    
    print("/nNo se encontró un texto llano satisfactorio.")
    return None

########################### Ejercicio 4 ###########################
#Función encriptarCifradoHill. Encriptar un mensaje con cifrado Hill. 
def encriptarCifradoHill(texto, matriz, dimension): 
    n = 26 # Módulo 26. A=0, B=1, ..., Z=25. 
    det = calculoDeterminante(matriz) # Calcular determinante de la matriz. 

    if comprobarCalculoInversa(n, det)==1: # Comprobar si se puede calcular la inversa modular, si no se puede calcular no se podrá desencriptar. 
        vector_texto = []
        texto_cifrado = []

        vector_texto = TextToNumber(texto)

        # Si el texto tiene el mismo largo que la dimensión 
        if len(vector_texto) == dimension: 

            texto_cifrado = encriptarMensaje(vector_texto, matriz, n)

            return texto_cifrado
    
        # Si el texto es de un largo distinto al de la dimensión 
        else: 
            # Si el texto es más pequeño que la dimensión se rellena con otro valor (A)
            if len(vector_texto) < dimension: 
                while len(vector_texto) < dimension: 
                    vector_texto.append(25) # Z=25, si el vector es más pequeño que la dimensión rellenamos con Z

                texto_cifrado = encriptarMensaje(vector_texto, matriz, n)
                
                return texto_cifrado

            # Si el texto es más largo que la dimensión-->se divide en bloques
            if len(vector_texto) > dimension:
                
                # range (start, stop, step)
                # Primer valor--> valor de inicio. 
                # Segundo valor--> límite superior. 
                # Tercer valor--> tamaño del paso. 
                for i in range(0, len(vector_texto), dimension):
                    bloque = []
                    
                    # Llenar el bloque hasta alcanzar el tamaño `dimension`
                    for j in range(dimension):
                        if i + j < len(vector_texto):  # Asegurarse de no exceder la longitud del vector
                            bloque.append(vector_texto[i + j])
                        else:
                            bloque.append(25)  # Si el bloque es más pequeño que `dimension`, rellenar con Z (25)

                    # Encriptar el bloque y agregarlo al texto cifrado
                    bloque_cifrado = encriptarMensaje(bloque, matriz, n)
                    texto_cifrado.extend(bloque_cifrado)

                return texto_cifrado

    else: 
        return -1

#Función desencriptarCifradoHill. Desencriptar un mensaje con cifrado Hill. 
def desencriptarCifradoHill(mensajeEncriptado, matriz, dimension):
    n = 26 # Módulo 26
    matriz_inversa = InvModMatrix(matriz, n) # Calcular la inversa modular la matriz. 

    texto_descifrado = []

    # range (start, stop, step)
    # Primer valor--> valor de inicio. 
    # Segundo valor--> límite superior. 
    # Tercer valor--> tamaño del paso. 
    for i in range(0, len(mensajeEncriptado), dimension): # Desde el valor 0 a lo largo del mensaje encriptdo ve de 3 en 3.
        # Crear un bloque de tamaño `dimension`
        bloque = []
        j = i
        while j < i + dimension and j < len(mensajeEncriptado): # j < i + dimension, para que se agreguen hasta <dimension> elementos
            bloque.append(mensajeEncriptado[j])
            j += 1

        # Si el bloque es menor que la dimensión, rellenar con 25 (equivalente a 'Z')
        while len(bloque) < dimension:
            bloque.append(25)

        bloque_descifrado = []
        for fila in range(len(matriz_inversa)): # Recorrer fila a fila la matriz. 
            aux = 0 # Utilizada para guardar el valor de la multiplicación fila*columna
            for colum in range(len(bloque)): # Recorrer columna a columna la matriz. 
                aux += matriz_inversa[fila][colum] * bloque[colum] # Calcular multiplicación de fila*columna
            
            bloque_descifrado.append(aux) 

        texto_descifrado.extend(bloque_descifrado) # Agregar el bloque descifrado al texto descifrado
        
    texto_descifrado = calcularModulo(texto_descifrado, n) 

    return texto_descifrado   

########################### Menú Afín #############################
def menu_cifrado_afín():
    global texto_cifrado  # Para acceder a la variable global
    
    while True:
        print("=== Cifrado Afín ===")
        print("1. Cifrar un mensaje")
        print("2. Adivinar valores de k y d")
        print("3. Salir")
        opcion = obtener_numero_entero("Elige una opción (1-3): ")
        print("\n")

        if opcion == 1:
            # Cifrar
            texto = input("Introduce el texto llano para cifrar con el cifrado afín: ")
            print("\n")
            k = obtener_numero_entero("Introduce el valor de k (debe ser coprimo con 26): ")
            d = obtener_numero_entero("Introduce el valor de d: ")
            texto_cifrado = afinCypher(texto, k, d)
            print("\n")
            print(f"El texto cifrado usando el cifrado afín es: {texto_cifrado}")
        
        elif opcion == 2:
            # Criptoanálisis para adivinar k y d
            
            texto_descifrado = afinCriptoanalisis(texto_cifrado)  # Usa afinCriptoanalisis directamente
            if texto_descifrado:
                print(f"Texto descifrado encontrado: {texto_descifrado}")
            else:
                print("No se encontró un texto llano satisfactorio.")
        
        elif opcion == 3:
            print("Saliendo del menú de Cifrado Afín.")
            break
        
        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 3.")

def menu_hill():

    while True:
    
        print("=== Cifrado Hill ===")
        print("1. Probar con matriz aleatoria ")
        print("2. Probar con valores predeterminados")
        print("3. Salir")
        op=obtener_numero_entero("Elige una de las opciones: ")
        print("\n")

        if op==1:
            texto = input("Introduce el texto llano para cifrar con el cifrado Hill: ")
            print("Si el texto es más corto que la dimensión de la matriz se rellenara con 'Z' \n")
            dimension = obtener_numero_entero("Introduce el valor de la dimension de la matriz: ")
            matriz = generarMatriz(dimension)

            encriptado=encriptarCifradoHill(texto, matriz, dimension)

            if encriptado != -1: # Si el encriptado se ha podido hacer con éxito. 
                print("El texto en cifrado Hill es: ", encriptado, "\n")

                desencriptado=desencriptarCifradoHill(encriptado, matriz, dimension)
                print("El texto en descifrado Hill es: ", desencriptado)
                print("Significado del mensaje desencriptado: ", NumberToText(desencriptado), "\n") # Cambiar los números por el carácter correspondiente para saber lo que pone.
            
            else : # Si el encriptado ha fallado. 
                print("No se puede cifrar.")
        
        elif op==2:
            texto = input("Introduce el texto llano para cifrar con el cifrado Hill: ")
            print("Si el texto es más corto que la dimensión de la matriz se rellenara con 'Z' \n")
            dimension = 3
            matriz = [ [ 6, 24, 1 ], [ 13, 16, 10 ], [ 20, 17, 15 ] ]

            encriptado=encriptarCifradoHill(texto, matriz, dimension)

            if encriptado != -1: # Si el encriptado se ha podido hacer con éxito. 
                print("El texto en cifrado Hill es: ", encriptado, "\n")

                desencriptado=desencriptarCifradoHill(encriptado, matriz, dimension)
                print("El texto en descifrado Hill es: ", desencriptado)
                print("Significado del mensaje desencriptado: ", NumberToText(desencriptado), "\n") # Cambiar los números por el carácter correspondiente para saber lo que pone.
            
            else : # Si el encriptado ha fallado. 
                print("No se puede cifrar.")
        
        elif op==3: 
            print("Saliendo del menú de Cifrado Hill.")
            break

        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 3.")

############################## Menú ###############################
#Aqui inicia el programa, primero pido que elija una opcion
def menu():
    
    while True:
        print("1. Cifrado Afin")
        print("2. Cifrado y descifrado Hill")
        print("3. Salir")
        op=obtener_numero_entero("Elige una de las opciones: ")
        print("\n")

        if op == 1: 
            menu_cifrado_afín()

        elif op == 2: 
            menu_hill()
        
        elif op == 3: 
            print("Saliendo\n")
            break
                
        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 3.")
menu()