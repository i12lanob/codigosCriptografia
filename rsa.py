###################################################################
# Práctica 4: Cifrado RSA                                         #
###################################################################
# Blanca Lara Notario                                             #
# Rafael Bueno Espinosa                                           #
# Francisco Bueno Espinosa                                        #
###################################################################
import re
###################################################################
#Funciones útiles                                                 #
###################################################################

###################################################################
#Funciones principales                                            #
###################################################################

########################### Ejercicio 1 ###########################
#Función primosolostra. 

#Función primoMillerRabin

########################### Ejercicio 2 ###########################
#Función keygeneration

########################### Ejercicio 3 ###########################
#Función textoACifras

########################### Ejercicio 4 ###########################
#Función preparenumcipher 

#Función preparetextdecipher 

########################### Ejercicio 5 ###########################
#Función rsacipher

#Función rsadecipher

########################### Ejercicio 6 ###########################
#Función rsaciphertext

#Función rsadeciphertext

########################### Ejercicio 7 ###########################
#Función rsaciphertextsign

########################### Ejercicio 8 ###########################
#Función rsadeciphertextsing

########################### Ejercicio 9 ###########################
#Función cifradoGamal

#Función descifradoGamal

############################## Menú ###############################
def menu():
    while True:
        print("1. Cifrado y descifrado por mochilas")
        print("2. Cifrado y descifrado con mochilas trampa")
        print("3. Encontrar mochila supercreciente")
        print("4. Salir")
        op = input("Elige una de las opciones: ")
        print("\n")

        op = int(op)

        if op == 1:
            s = []
            print("Introduce los valores de la mochila. Escribe 'fin' para terminar:")
            while True:
                entrada = input("Número: ")
                if entrada.lower() == "fin":  # Salimos si el usuario escribe 'fin'
                    break
                try:
                    numero = int(entrada)  # Convertimos a entero
                    s.append(numero)  # Añadimos el número al vector
                except ValueError:
                    print("Por favor, introduce un número válido o 'fin'.")

            if knapsack(s) == 1 or knapsack(s) == 0:
                texto = input("Introduce un texto a cifrar: ")
                cadena = knapsackcipher(s, texto)  # Asegúrate de que esta función esté implementada
                print("El texto cifrado es:", cadena, "\n")
                texto_descifrado = knapsackdecipher(s, cadena)  # Verifica también esta función
                print("El texto descifrado es:", texto_descifrado, "\n")

            else: 
                print("No es una mochila\n")

        elif op == 2:
            s = []
            print("Introduce los valores de la mochila. Escribe 'fin' para terminar:")
            while True:
                entrada = input("Número: ")
                if entrada.lower() == "fin":
                    break
                try:
                    numero = int(entrada)
                    s.append(numero)
                except ValueError:
                    print("Por favor, introduce un número válido o 'fin'.")

            if knapsack(s) == 1:



                m = obtener_numero_entero("Introduce el valor de m: ")

                if not comprobar_valor_m(m, s):
                    print("El valor de m debe ser mayor que la suma de los valores de la mochila.\n")
                    continue

                w = elegir_w(m, s)

                # Generar clave pública y realizar cifrado/descifrado
                cadena_privada = knapsackpublicandprivate(s, m, w)
                texto = input("Introduce el texto a cifrar con la mochila trampa: ")
                
                cadena_cifrada = knapsackcipher(cadena_privada, texto)
                print("El texto cifrado es:", cadena_cifrada)

                texto_descifrado = knapsackdeciphermh(s, m, w, cadena_cifrada)
                print("El texto descifrado es:", texto_descifrado, "\n")
            
            else: 
                print("No es una mochila supercreciente o no es una mochila\n")

        elif op == 3:
            #mochila_trampa = [ 4500, 9000, 18000, 36000, 72000] #m 5000003
            #mochila_trampa = [13, 9, 7, 6] 
            #mochila_trampa = [ 123, 256, 512, 1024, 2048] #m=100003, con rango 2
            #mochila_trampa = [23, 46, 92, 184, 368] #m=104729 a la primera
            mochila_trampa = []
           
            print("Introduce los valores de la mochila. Escribe 'fin' para terminar:")
            while True:
                entrada = input("Número: ")
                if entrada.lower() == "fin":
                    break
                try:
                    numero = int(entrada)
                    mochila_trampa.append(numero)
                except ValueError:
                    print("Por favor, introduce un número válido o 'fin'.")

            m = obtener_numero_entero("Introduce el valor de m: ")
            i = 0  # Rango inicial
            vector = shamirZimmel(m, mochila_trampa, i)

            if vector != -1:
                print("El vector supercreciente encontrado es:", vector, "\n")
            else:
                print("No se pudo encontrar un vector supercreciente para el rango dado.\n")
            
        elif op == 4:
            print("Saliendo del programa.\n")
            break

        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 4.\n")

menu()