###################################################################
# Práctica 4: Cifrado RSA                                         #
###################################################################
# Blanca Lara Notario                                             #
# Rafael Bueno Espinosa                                           #
# Francisco Bueno Espinosa                                        #
###################################################################
import re
import random
import time 
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

###################################################################
#Funciones principales                                            #
###################################################################

########################### Ejercicio 1 ###########################
#Función primosolostra. 
def primosolostra(n, iter): 
    
    if n <= 1:
        return False
    
    if n == 2:
        return True

    # Asegurarse que n sea impar
    if n % 2 == 0:
        return False
    
    def simbolo_legendre(a, n):
        # Calcular el símbolo de Legendre (a/n) usando el criterio de Euler
        if a % n == 0:
            return 0
        
        # Si a^(n-1)/2 % n == 1, entonces es un residuo cuadrático (símbolo 1)
        aux = pow(a, (n - 1) // 2, n)
        
        if aux == 1:
            return 1
        elif aux == n - 1:  # si a^(n-1)/2 ≡ -1 mod n
            return -1
        
        return 0
    
    for _ in range(iter): # Iteramos varias veces para probar el valor de n

        a = random.randint(2, n-1) # Generar una a aleatoria entre 2 y n-2
        u=pow(a, (n-1)//2, n) # Calcular a ^ ((n-1)/2) mod(n)
        v = simbolo_legendre(a, n)

        if u != v % n: 
            return False
    
    return True

#Función primoMillerRabin

#Función testPrimos. Llama a primosolostra y primoMillerRabin para calcular la probabilidad de que sea pseudoprimo.                
def testPrimos(rango, iter):
    for n in range(2, rango): 

        # Medición del tiempo de inicio del rango
        start_time = time.perf_counter() # Función de la biblioteca time para medir el tiempo de forma precisa.
        
        esPrimoOlostra = primosolostra(n, iter)
        
        # Medición del tiempo de finalización del rango
        end_time = time.perf_counter() # Función de la biblioteca time para medir el tiempo de forma precisa.
        elapsed_time = end_time - start_time # Calculamos el tiempo restando el final y el inicial.

        if esPrimoOlostra:
            print(f"{n} pasó el test de Solovay-Strassen")
            prob=(1/2)**iter
            #prob=1/(2**iter)
            print(f"Probabilidad de que sea pseudo-primo: {prob}\n")

            #break
        else:
            print(f"{n} NO pasó el test de Solovay-Strassen")

        print(f"Tiempo requerido en el rango: {elapsed_time:.4f} segundos\n")  # Imprimimos el valor
        
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
        print("2. Salir")
        op = input("Elige una de las opciones: ")
        print("\n")

        op = int(op)

        if op == 1:
            rango = obtener_numero_entero("Introduce un valor para el rango: ")
            iter = obtener_numero_entero("Introduce un valor para el número de iteraciones: ")
            testPrimos(rango, iter)
        elif op == 2:
            print("Saliendo del programa.\n")
            break

        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 4.\n")

menu()