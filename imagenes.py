###################################################################
# Práctica 5: Esteganografía 1                                    #
###################################################################
# Blanca Lara Notario                                             #
# Rafael Bueno Espinosa                                           #
# Francisco Bueno Espinosa                                        #
###################################################################
import re
from PIL import Image
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
def LSBsimplecypher(image_path, message, output_path):
    # Cargar la imagen en modo de escala de grises
    img = Image.open(image_path).convert('L') # Carga la imagen con open() y la convierte a escala de grises con convert('L')
    pixels = img.load() # Carga y devuelve una matriz bidimensional para poder modificar la 

    # Convertir el mensaje a bits (usando las funciones proporcionadas)
    message_bits = ''.join(texttobit(message)) + '00000000'  # Añade un terminador nulo al final
    message_length = len(message_bits)

    # Verificar si la imagen tiene suficientes píxeles para ocultar el mensaje
    width, height = img.size
    if message_length > width * height:
        raise ValueError("La imagen es demasiado pequeña para ocultar el mensaje.")

    # Modificar los primeros píxeles con los bits del mensaje
    bit_index = 0
    for y in range(height):
        for x in range(width):
            if bit_index < message_length:
                # Obtener el valor del píxel
                pixel_value = pixels[x, y]  
                # Convertir el bit actual del mensaje a entero (0 o 1)
                bit_actual = int(message_bits[bit_index])
                # Si el bit es 1, forzamos el LSB a 1. Si es 0, forzamos el LSB a 0.
                if bit_actual == 1:
                    new_pixel_value = pixel_value | 1  # Fuerza el LSB a 1
                else:
                    new_pixel_value = pixel_value & ~1  # Fuerza el LSB a 0
                # Actualizar el valor del píxel
                pixels[x, y] = new_pixel_value
                bit_index += 1

    # Guardar la imagen modificada
    img.save(output_path)
    print(f"Mensaje ocultado y guardado en {output_path}")
    
#Función LSBsimpledecypher
def LSBsimpledecypher(image_path):
    from PIL import Image  # Asegúrate de que la librería esté importada

    # Cargar la imagen en escala de grises
    img = Image.open(image_path).convert('L')
    pixels = img.load()

    # Extraer los bits del LSB de los píxeles
    width, height = img.size
    bits = ''
    for y in range(height):
        for x in range(width):
            pixel_value = pixels[x, y]
            # Añadir el LSB del píxel a la cadena de bits
            bits += str(pixel_value & 1)

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

#Función LSBcomplexdecypher


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

########################### Ejercicio 3 ###########################
#Función desordenaimagen

#Función ordenaimgane

########################### Ejercicio 4 ###########################
#Función desordenaimagenite

#Función ordenaimagenite

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
        print("5. Salir")
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
            image_path = input("Ingrese el nombre de la imagen de entrada (ej. input.png): ")
            message = input("Ingrese el mensaje que desea ocultar: ")
            output_path = input("Ingrese el nombre de la imagen de salida (ej. output.png): ")
            try:
                LSBsimplecypher(image_path, message, output_path)
            except Exception as e:
                print(f"Error: {e}")
        
        elif op == 4:
            image_path = input("Ingrese el nombre de la imagen con el mensaje oculto (ej. output.png): ")
            try:
                mensaje_recuperado = LSBsimpledecypher(image_path)
                print(f"Mensaje recuperado: {mensaje_recuperado}")
            except Exception as e:
                print(f"Error: {e}")
        elif op == 5:
            print("Saliendo del programa.\n")
            break

        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 5.\n")

menu()