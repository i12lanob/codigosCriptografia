###################################################################
# Práctica 5: Esteganografía 1                                    #
###################################################################
# Blanca Lara Notario                                             #
# Rafael Bueno Espinosa                                           #
# Francisco Bueno Espinosa                                        #
###################################################################
import re
from PIL import Image
import numpy as np
###################################################################
#Funciones útiles                                                 #
###################################################################
#Función obtener_numero_entero. Comprobar que solo se introducen números
def obtener_numero_entero(mensaje):
    while True:
        entrada = input(mensaje)
        if entrada.isdigit():
            return int(entrada)
        else:
            print("Por favor, introduce solo dígitos.\n")

#Función algeucl. Calcula el MCD de a y b usando el Algoritmo de Euclides.
def algeucl(a,b): 
    while(b!=0) :
        temp=b # Crear una variable temporal para guardar b
        b=a%b # Actualizar b con el resto de a y b (nuevo divisor)
        a=temp # Actualizar a (nuevo dividendo)
    return a

#Función formatoImagen. Comprobamos si la imagen es de formato ".png"
def formatoImagen(imagen):
    return imagen.endswith(".png") #endswith mira el sufijo del texto

def calcularDeterminante(A):
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

        det += signo * A[0][col] * calcularDeterminante(submatriz) # Sumar el producto del signo, el elemento y el determinante de la submatriz

    return det

#Aunque en Python hay una forma más rápida de calcular las matrices inversas, vamos a utilizar las funciones de la práctica 1
#Función InvModMatrix. Calcula la inversa de una matriz en el módulo n si existe.
def InvModMatrix(A, n):

    # Calcular determinante de la matriz A
    det = calcularDeterminante(A)
    det = det % n

    #Función invmod. Inversa de p en n 
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
            
    det_inv = invmod(det, n) # Calcular determinante inverso

    #Función matrizTraspuesta
    def matrizTraspuesta(A):

        submatriz = []
        for col in range(len(A)): 
            nueva_fila = []
            for fil in range(len(A)): 
                nueva_fila.append(A[fil][col]) # Intercambiar las filas por columnas

            submatriz.append(nueva_fila)

        return submatriz
    
    traspuesta = matrizTraspuesta(A) 

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
                cofactor = signo * calcularDeterminante(submatriz) 

                # Añadir el cofactor a la fila adjunta
                fila_adjunta.append(cofactor)

            # Añadir la fila adjunta a la matriz de adjunta
            adjunta.append(fila_adjunta)

        return adjunta

    adjunta = matrizAdjunta(traspuesta)

    # Una vez obtenida la matriz adjunta se calcula la inversa modular
    inversa_modular = []
    for fila in adjunta:
        fila_inversa = []
        for elem in fila:
            fila_inversa.append((det_inv * elem) % n)
        inversa_modular.append(fila_inversa)

    return inversa_modular
###################################################################
#Funciones principales                                            #
###################################################################

############################ Método LSB ###########################
########################### Ejercicio 2 ###########################
#Función texttobit
def texttobit(texto):
    texto = texto.upper() 
    cadena_numerica= []

    # Primero transformar binario a ASCII
    for char in texto:
        if 'A' <= char <= 'Z':  # Solo considerar letras
            letra = ord(char) # Transformar de letra a ASCII
            cadena_numerica.append(letra)

    cadenaBit = []

    # Pasamos ASCII a binario
    for num in cadena_numerica:
        #Transformar a binario. En este caso un número binario (b) de 8 caracteres y rellenar con 0 (a la izquierda)
        binario = format(num, '08b') #format permite especificar el formato. 
        cadenaBit.append(binario)
        
    return cadenaBit
    
#Función bittotext
def bittotext(cadena_bit):
    texto = ""
    ascii = []
    #Primero pasamos el binario a ASCII
    for binario in cadena_bit:
        # Convertir binario a entero y luego a carácter ASCII
        ascii.append(int(binario, 2)) # Pasamos a su equivalente numerico 

    # Pasamos ASCII a letra
    for num in ascii: 
        caracter = chr(num)
        texto += caracter

    return texto

########################### Ejercicio 3 ###########################
#Función LSBsimplecypher
def LSBsimplecypher(ruta_entrada, message, ruta_salida):
    # Cargar la imagen en modo de escala de grises
    img = Image.open(ruta_entrada).convert('L') # Carga la imagen con open() y la convierte a escala de grises con convert('L')
    pixels = img.load() # Carga y devuelve una matriz bidimensional para poder modificar la 

    # Convertir el mensaje a bits (usando las funciones proporcionadas)
    bits_mensaje = ''.join(texttobit(message)) + '00000000'  # Añade un terminador nulo al final
    longitud_mensaje = len(bits_mensaje)

    # Verificar si la imagen tiene suficientes píxeles para ocultar el mensaje
    anchura, altura = img.size
    if longitud_mensaje > anchura * altura:
        raise ValueError("La imagen es demasiado pequeña para ocultar el mensaje.")

    # Modificar los primeros píxeles con los bits del mensaje
    bit_index = 0
    for y in range(altura):
        for x in range(anchura):
            if bit_index < longitud_mensaje:
                # Obtener el valor del píxel
                valor_pixel = pixels[x, y]  
                # Convertir el bit actual del mensaje a entero (0 o 1)
                bit_actual = int(bits_mensaje[bit_index])
                # Si el bit es 1, forzamos el LSB a 1. Si es 0, forzamos el LSB a 0.
                if bit_actual == 1:
                    nuevo_valor_pixel = valor_pixel | 1  # Fuerza el LSB a 1
                else:
                    nuevo_valor_pixel = valor_pixel & 0  # Fuerza el LSB a 0
                # Actualizar el valor del píxel
                pixels[x, y] = nuevo_valor_pixel
                bit_index += 1

    # Guardar la imagen modificada
    img.save(ruta_salida)
    print(f"Mensaje ocultado y guardado en {ruta_salida}")
    
#Función LSBsimpledecypher
def LSBsimpledecypher(ruta_entrada):
    # Cargar la imagen en escala de grises
    img = Image.open(ruta_entrada).convert('L')
    pixels = img.load()

    # Extraer los bits del LSB de los píxeles
    anchura, altura = img.size
    bits = ''
    for y in range(altura):
        for x in range(anchura):
            valor_pixel = pixels[x, y]
            # Añadir el LSB del píxel a la cadena de bits
            bits += str(valor_pixel & 1)

    # Convertir los bits en grupos de 8
    mensaje_bits = []
    byte = ''  # Variable temporal para almacenar los 8 bits
    for bit in bits:
        byte += bit  # Añadir un bit a la variable 'byte'
        if len(byte) == 8:  # Cuando tengamos 8 bits
            mensaje_bits.append(byte)  # Añadir el "byte" completo a la lista
            byte = ''  # Reiniciar la variable 'byte' para el siguiente conjunto de 8 bits

    # Convertir los bytes en texto
    mensaje = bittotext(mensaje_bits)

    # Detenerse al encontrar el terminador nulo (00000000)
    if '\x00' in mensaje:
        mensaje = mensaje.split('\x00')[0]  # Cortar el mensaje donde aparece el terminador

    return mensaje
########################### Ejercicio 4 ###########################
#Función LSBcomplexcypher
def LSBcomplexcypher(ruta_entrada, message, ruta_salida, s):
    # Cargar la imagen en modo de escala de grises
    img = Image.open(ruta_entrada).convert('L')
    pixels = img.load()

    # Convertir el mensaje a bits (usando las funciones proporcionadas)
    bits_mensaje = ''.join(texttobit(message)) + '00000000'  # Añadir un terminador nulo
    longitud_mensaje = len(bits_mensaje)

    # Verificar si la imagen tiene suficientes píxeles para ocultar el mensaje con el salto s
    anchura, altura = img.size
    total_pixels = anchura * altura
    max_longitud_mensaje = total_pixels // s  # Número máximo de bits que se pueden ocultar con el salto s
    if longitud_mensaje > max_longitud_mensaje:
        raise ValueError("La imagen es demasiado pequeña para ocultar el mensaje con el salto especificado.")

    # Modificar los píxeles seleccionados con el salto s
    bit_index = 0
    for index in range(s - 1, total_pixels, s):  # Salta de s en s píxeles
        x = index % anchura  # Para calcular las coordenadas x (horizontal)
        y = index // anchura  # Para calcular las coordenadas y (vertical)

        if bit_index < longitud_mensaje:
            valor_pixel = pixels[x, y]
            # Convertir el bit actual del mensaje a entero (0 o 1)
            bit_actual = int(bits_mensaje[bit_index])
            # Modificar el LSB del píxel con el bit correspondiente del mensaje
            if bit_actual == 1:
                nuevo_valor_pixel = valor_pixel | 1  # Fuerza el LSB a 1
            else:
                nuevo_valor_pixel = valor_pixel & 0  # Fuerza el LSB a 0
            pixels[x, y] = nuevo_valor_pixel  # Actualizar el píxel
            bit_index += 1

    # Guardar la imagen modificada
    img.save(ruta_salida)
    print(f"Mensaje ocultado y guardado en {ruta_salida}")
#Función LSBcomplexdecypher
def LSBcomplexdecypher(ruta_entrada, s):
    # Cargar la imagen en escala de grises
    img = Image.open(ruta_entrada).convert('L')
    pixels = img.load()

    # Extraer los bits del LSB de los píxeles con el salto s
    anchura, altura = img.size
    bits = ''
    total_pixels = anchura * altura
    for index in range(s - 1, total_pixels, s):  # Salta de s en s píxeles
        x = index % anchura  # Para calcular las coordenadas x (horizontal)
        y = index // anchura  # Para calcular las coordenadas y (vertical)
        valor_pixel = pixels[x, y]
        bits += str(valor_pixel & 1)  # Extraer el LSB

    # Convertir los bits en grupos de 8
    mensaje_bits = []
    byte = ''  # Variable temporal para almacenar los 8 bits
    for bit in bits:
        byte += bit  # Añadir un bit a la variable 'byte'
        if len(byte) == 8:  # Cuando tengamos 8 bits
            mensaje_bits.append(byte)  # Añadir el "byte" completo a la lista
            byte = ''  # Reiniciar la variable 'byte' para el siguiente conjunto de 8 bits

    # Convertir los bytes en texto
    mensaje = bittotext(mensaje_bits)

    # Detenerse al encontrar el terminador nulo (00000000)
    if '\x00' in mensaje:
        mensaje = mensaje.split('\x00')[0]  # Cortar el mensaje donde aparece el terminador

    return mensaje

##################### Desordenando una imagen #####################
########################### Ejercicio 1 ###########################
#Función isinvertible
def isinvertible(A, n):

    # Calcular determinante de la matriz A
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det = det % n

    # Si el mcd==1 del determinante y de n entonces se puede calcular la inversa modular
    if algeucl(n, det) == 1:
        return True
    
    print("El valor n y el determinante de la matriz tienen que ser coprimos\n")
    return False
########################### Ejercicio 2 ###########################
#Función powinverse
def powinverse(A, n):
    # Asegurarse de que A es una matriz cuadrada
    if A.shape[0] != A.shape[1]: # Shape devuelve las dimensiones de la matriz
        raise ValueError("La matriz A debe ser cuadrada.\n")
    
    # Crear la matriz identidad
    I = np.eye(A.shape[0]) # eye crea la matriz idenditidad (si es np.eye(3) crea la matriz idendidad de 3x3)
    
    potencia = I

    # Calcular potencias de A hasta el límite n
    for p in range(1, n + 1):
        potencia = np.dot(potencia, A)  # Calcular A^p. dot calcula el producto matricial 
        if np.allclose(potencia, I): # allclose compara dos matrices
            return p
    
    # Si no se encuentra una p
    return -1

########################### Ejercicio 3 ###########################
#Función desordenaimagen
def desordenaimagen(A, imagen, output_path):
    # Cargar la imagen en modo de escala de grises
    img = Image.open(imagen).convert('L') # Carga la imagen con open() y la convierte a escala de grises con convert('L')
    matriz_imagen = np.array(img) # Convertir a array la imagen 

    fil, col = matriz_imagen.shape # Cogemos las dimensiones de la imagen para comprobar si es cuadrada
    if fil != col: # Comprobamos si es una imagen cuadrada
        raise Exception("La imagen no tiene una dimensión cuadrada\n")
    
    # Comprobamos si la matriz es invertible mod nn (fil)
    if not isinvertible(A, fil): # Cogemos fil pero puede ser también col, ya que tienen que tener el mismo valor
        raise Exception("La matriz no es invertible\n")

     # Crear una nueva matriz para almacenar la imagen desordenada
    desordenada = np.zeros_like(matriz_imagen) # Rellena de 0 la matriz

    for i in range(fil):
        for j in range(col):
            # Coordenada original
            coord = np.array([i, j])
            # Transformación de coordenadas
            nueva_coord = np.dot(A, coord) % fil # dot es el producto matricial

            # Asegurarse de que las nuevas coordenadas estén dentro del rango
            x, y = nueva_coord
            if 0 <= x < fil and 0 <= y < col:
                desordenada[x, y] = matriz_imagen[i, j]

    # Guardamos esta nueva imagen desordenada
    img_desordenada = Image.fromarray(desordenada) # fromarray convierte de array a imagen
    img_desordenada.save(output_path)
    print("Se ha realizado con exito\n")
#Función ordenaimgane
def ordenaimagen(A, imagen, output_path):
    img = Image.open(imagen) # Abrimos la imagen
    n = np.array(img).shape[0]

    # Calculamos la inversa de A en mod n, usando funciones que hemos definido en prácticas anteriores
    A_inv = np.array(InvModMatrix(A,n))  # np.array para pasar una lista a un array Numpy

    # Una vez calculamos la inversa llamamos la función desordenaimagen, con la inversa de la matriz
    return desordenaimagen(A_inv, imagen, output_path) 

########################### Ejercicio 4 ###########################
#Función desordenaimagenite
def desordenaimagenite(A, imagen, output_path):
    # Cargar la imagen en modo de escala de grises
    img = Image.open(imagen).convert('L')
    matriz_imagen = np.array(img)
    
    fil, col = matriz_imagen.shape  # Dimensiones de la imagen
    
    if fil != col:
        raise Exception("La imagen no tiene una dimensión cuadrada\n")
    
    n = fil  # Usamos el tamaño de la imagen como n
    
    # Encontrar valores válidos de k (de 1 a n) tales que A^k sea invertible
    valid_k_values = []
    for k in range(1, n + 1):
        A_k = np.linalg.matrix_power(A, k) % n
        if isinvertible(A_k, n):  # Llamamos a la función isinvertible para verificar si A^k es invertible
            valid_k_values.append(k)
    
    # Informar al usuario los valores válidos de k
    if valid_k_values:
        print(f"Los valores válidos de k para los cuales A^k es invertible son: {valid_k_values}")
    else:
        print("No se han encontrado valores de k para los cuales A^k sea invertible.")
        return
    
    # Pedir al usuario un valor k válido
    while True:
        try:
            k = int(input(f"Introduce un valor entero k para calcular A^k (elige entre {valid_k_values}): "))
            if k not in valid_k_values:
                print(f"Por favor, introduce un número entero válido entre {valid_k_values}.")
                continue
            break
        except ValueError:
            print("Entrada no válida. Por favor, introduce un número entero.")
    
    # Calculamos A^k
    A_k = np.linalg.matrix_power(A, k) % n  # A^k módulo n
    
    # Verificamos si A^k es invertible
    if not isinvertible(A_k, n):
        raise Exception(f"A^k no es invertible para k={k}")
    
    # Crear una nueva matriz para almacenar la imagen desordenada
    desordenada = np.zeros_like(matriz_imagen)

    # Transformar las coordenadas de la imagen utilizando A^k
    for i in range(fil):
        for j in range(col):
            coord = np.array([i, j])
            nueva_coord = np.dot(A_k, coord) % n  # Transformación de las coordenadas
            x, y = nueva_coord
            if 0 <= x < fil and 0 <= y < col:
                desordenada[x, y] = matriz_imagen[i, j]

    # Guardamos la nueva imagen desordenada
    img_desordenada = Image.fromarray(desordenada)
    img_desordenada.save(output_path)
    print(f"Imagen desordenada con A^{k} guardada en {output_path}")

#Función ordenaimagenite
def ordenaimagenite(A, imagen, output_path):
    # Cargar la imagen desordenada
    img = Image.open(imagen)
    n = np.array(img).shape[0]  # Obtener el tamaño de la imagen (suponemos que es cuadrada)
    
    # Pedir al usuario el valor de k usado para desordenar la imagen
    while True:
        try:
            k = int(input("Introduce el valor de k usado para desordenar la imagen: "))
            if k <= 0:
                print("Por favor, introduce un número entero positivo.")
                continue
            
            # Calculamos A^k
            A_k = np.linalg.matrix_power(A, k) % n
            
            # Ahora calculamos la inversa de A^k módulo n
            if isinvertible(A_k, n):  # Verifica que A^k es invertible
                A_k_inv = InvModMatrix(A_k, n)  # Usa InvModMatrix o la función adecuada para la inversa modular
                # Llamamos a la función desordenaimagenite con A^k_inv
                desordenaimagenite(A_k_inv, imagen, output_path)
                break
            else:
                print(f"A^k no es invertible para k={k}. Intenta otro valor.")
        
        except ValueError:
            print("Entrada no válida. Por favor, introduce un número entero.")
########################### Ejercicio 5 ###########################
#Función desordenaimagenproceso

#Función desordenaimagenite

############################## Menú ###############################
def menu():

    while True:
        print("1. Texto a binario")
        print("2. Comprobar si matriz es invertible")
        print("3. Cifrar un texto en una imagen")
        print("4. Descifrar un texto de una imagen")
        print("5. Cifrar un mensaje en una imagen LSB Complex")
        print("6. Descifrar un mensaje de una imagen LSB Complex")
        print("7. Primer invertible en la matriz")
        print("8. Desordenar imagen")
        print("9. Ordenar imagen")
        print("10.Desordenar imagen K")
        print("11.Ordenar imagen K")
        print("12. Salir")
        op = int(input("Elige una de las opciones: "))
        print("\n")

        if op == 1: 
            texto=input("Introduce un texto a transformar en binario: ")
            cadena = texttobit(texto)
            print(f"La cadena {texto} es: {cadena}\n")
            print(f"La cadena {bittotext(cadena)}\n")
        elif op == 2:
            matriz = [[2 , 2] , [2 , 2]]
            n = 4
            if isinvertible(matriz, n): 
                print("Es invertible\n")

        elif op== 3:
            ruta_entrada = input("Ingrese el nombre de la imagen de entrada (ej. input.png): ")
            if formatoImagen(ruta_entrada):
                message = input("Ingrese el mensaje que desea ocultar: ")
                ruta_salida = input("Ingrese el nombre de la imagen de salida (ej. output.png): ")
                if formatoImagen(ruta_salida):
                    try:
                        LSBsimplecypher(ruta_entrada, message, ruta_salida)
                    except Exception as e:
                        print(f"Error: {e}")
                else: 
                    print("Tiene que ser formato png\n")
            else: 
                print("Tiene que ser formato png\n")
        
        elif op == 4:
            ruta_entrada = input("Ingrese el nombre de la imagen con el mensaje oculto (ej. output.png): ")
            if formatoImagen(ruta_entrada):
                try:
                    mensaje_recuperado = LSBsimpledecypher(ruta_entrada)
                    print(f"Mensaje recuperado: {mensaje_recuperado}")
                except Exception as e:
                    print(f"Error: {e}")
            else: 
                print("Tiene que ser formato png\n")

        elif op == 5:
            ruta_entrada = input("Ingrese el nombre de la imagen de entrada (ej. input.png): ")
            message = input("Ingrese el mensaje que desea ocultar: ")
            ruta_salida = input("Ingrese el nombre de la imagen de salida (ej. output.png): ")
            s = int(input("Ingrese el valor de salto (s): "))
            try:
                LSBcomplexcypher(ruta_entrada, message, ruta_salida, s)
            except Exception as e:
                print(f"Error: {e}")

        elif op == 6:
            ruta_entrada = input("Ingrese el nombre de la imagen con el mensaje oculto (ej. output.png): ")
            s = int(input("Ingrese el valor de salto (s): "))
            try:
                mensaje_recuperado = LSBcomplexdecypher(ruta_entrada, s)
                print(f"Mensaje recuperado: {mensaje_recuperado}")
            except Exception as e:
                print(f"Error: {e}")
        
        elif op == 7:
            A =  np.array([[0, 1],[1, 0]])
            n = obtener_numero_entero("Introduce un valor para n: ")
            p =powinverse(A, n)
            if p != -1: 
                print(f"El primer p es: {p}\n")
            else: 
                print("No hay p\n")

        elif op == 8:
            image_path = input("Ingrese el nombre de la imagen a desordenar (ej. imagen.png): ")
            if formatoImagen(image_path):
                output_path = input("Ingrese el nombre de la imagen desordenada (ej. desordenada.png): ")
                if formatoImagen(output_path):
                    #A = np.array([[2,1], [1,1]])
                    A = np.array([[1,5], [2,3]])
                    desordenaimagen(A, image_path, output_path)
                else: 
                    print("Tiene que ser formato png\n")
            else: 
                print("Tiene que ser formato png\n")

        elif op == 9: 
            image_path = input("Ingrese el nombre de la imagen desordenada (ej. desordenada.png): ")
            if formatoImagen(image_path):
                output_path = input("Ingrese el nombre de la imagen ordenada (ej. ordenada.png): ")
                if formatoImagen(output_path):
                    #A = np.array([[2,1], [1,1]])
                    A = np.array([[1,5], [2,3]])
                    ordenaimagen(A, image_path, output_path)
                else: 
                    print("Tiene que ser formato png\n")
            else: 
                print("Tiene que ser formato png\n")

        elif op == 10:  # Supongamos que esta es la nueva opción para desordenaimagenite
            image_path = input("Ingrese el nombre de la imagen a desordenar con potencia k (ej. imagen.png): ")
            if formatoImagen(image_path):
                output_path = input("Ingrese el nombre de la imagen desordenada (ej. desordenada_k.png): ")
                if formatoImagen(output_path):
                    # Puedes cambiar la matriz según tus necesidades
                    A = np.array([[1, 1], [1, 2]])  
                    try:
                        desordenaimagenite(A, image_path, output_path)
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("El nombre de salida debe tener formato png.\n")
            else:
                print("El nombre de entrada debe tener formato png.\n")

        elif op == 11:  # Nueva opción para ordenar la imagen usando A^k
            image_path = input("Ingrese el nombre de la imagen desordenada (ej. desordenada.png): ")
            if formatoImagen(image_path):
                output_path = input("Ingrese el nombre de la imagen ordenada (ej. ordenada.png): ")
                if formatoImagen(output_path):
                    # Define la matriz A que fue utilizada para desordenar
                    A = np.array([[1, 1], [1, 2]])
                    try:
                        ordenaimagenite(A, image_path, output_path)
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("El nombre de salida debe tener formato png.\n")
            else:
                print("El nombre de entrada debe tener formato png.\n")
        elif op == 12:
            print("Saliendo del programa.\n")
            break

        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 5.\n")

menu()