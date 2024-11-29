###################################################################
# Práctica 5: Esteganografía 1                                    #
###################################################################
# Blanca Lara Notario                                             #
# Rafael Bueno Espinosa                                           #
# Francisco Bueno Espinosa                                        #
###################################################################
import re
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

#Función LSBsimpledecypher

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
        print("3. Salir")
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
        
        elif op == 3:
            print("Saliendo del programa.\n")
            break

        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 4.\n")

menu()
