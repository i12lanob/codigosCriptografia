import re

###################################################################
#Funciones útiles                                                 #
###################################################################
#Función TextToNumber: Tranformar una cadena Ascii a letra
def TextToNumber(texto):
    
    texto = texto.upper()  # Convertir el texto a mayúsculas para facilitar el mapeo
    cadena_numerica = []
    
    for char in texto:
        if 'A' <= char <= 'Z':  # Solo considerar letras
            var=letter2ascii(char)
            cadena_numerica.append(var)
    
    return cadena_numerica

#def NumberToText(num):
#    cadena_numerica = []
#    
#    
#    for n in texto:
#       var=ascii2letter(n)
#        cadena_numerica.append(var)
#    
#    return cadena_numerica



###################################################################
#Funciones principales                                            #
###################################################################

########################### Ejercicio 1 ###########################
#Función letter2ascii

#Función ascii2letter

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
texto = input("Introduce el texto llano para cifrar con el cifrado afín: ")

