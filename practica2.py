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
#Función knapsack.

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