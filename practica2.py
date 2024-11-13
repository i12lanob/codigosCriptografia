###################################################################
#Práctica 3: Cifrado por Mochilas y Mochilas trampa               #
###################################################################
#Blanca Lara Notario                                              #
#Rafael Bueno Espinosa                                            #
#Francisco Bueno Espinosa                                         #
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
            print("Por favor, introduce solo dígitos.")

#Función TextToNumber. Se pasa una cada de texto y se pasa a ASCII. 
def TextToNumber(texto):
    
    texto = texto.upper()  # Convertir el texto a mayúsculas para facilitar el mapeo
    cadena_numerica = []
    
    for char in texto:
        if 'A' <= char <= 'Z':  # Solo considerar letras
            var=letter2ascii(char) # Llamar a la función que transforme la letra en ASCII
            cadena_numerica.append(var)
    
    return cadena_numerica

###################################################################
#Funciones principales                                            #
###################################################################

########################### Ejercicio 1 ###########################
#Función letter2ascii
def letter2ascii(letra): 
    letra = letra.upper() 
    letra = ord(letra) # Transformar de letra a ASCII
    
    return letra

#Función ascii2letter
def ascii2letter(letra):   
    # Convertimos el código ASCII a la letra que 
    letra = chr(letra)
    
    # Mostramos el resultado
    return letra

########################### Ejercicio 2 ###########################
#Función knapsack. Mochila supercreciente, no supercreciente o no es una mochila.
def knapsack(vector_fila):
    suma = 0
    for i in range(len(vector_fila)): # Primero mira si alguno de los valores es negativo
        if (vector_fila[i] < 0):
            return -1 # Si es negativo no es una mochila 
       
    for i in range (len(vector_fila)): 
        suma += vector_fila[i]
        if suma < vector_fila[i+1]: # Si suma < vector_fila[i+1], es no supercreciente
            return 0
        
    return 1 # Es una mochila super creciente si el valor de la suma < vector_fila[i+1]

#Función knapsacksol.

#Función knapsackcipher.

#Función knapsackdecipher.

########################### Ejercicio 3 ###########################
#Función commonfactors.

#Función knapsackpublicandprivate.

#Función knapsackdeciphermh.

########################### Ejercicio 4 ###########################

############################## Menú ###############################
print("1. Cadena a ASCII")
print("2. ASCII a letra")
print("3. Comprobar si es mochila, supercreciente o no supercreciente")
op=input("Elige una de las opciones: ")
op=int(op)

if op == 1: 
    texto = input("Introduce el texto llano para cifrar con el cifrado afín: ")
    print("La cadena ", texto, " en ASCII es ", TextToNumber(texto))

if op == 2:
    ascii = obtener_numero_entero("Introduce el valor de ascii: ")
    if ascii>=65 and ascii<=90: 
        print("El valor ", ascii, " en letra es ", ascii2letter(ascii))
    else: 
        print("El valor debe estar entre 65 y 90 (incluidos)")

if op == 3: 
    vector_fila = [2, 5, 6, 10]
    aux = knapsack(vector_fila)

    if aux == 1: 
        print("Mochila supercreciente\n")

    elif aux == 0: 
        print("Mochila no supercreciente\n")
    
    else :
        print("No es mochila\n")
