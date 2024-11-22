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


#Función generarN. Generar una n aleatoria en un rango dado.
def generarN(rango1, rango2, nGeneradas):
    while True:
        n = random.randint(rango1, rango2)
        if n not in nGeneradas:  # Si n no está en la lista, lo añadimos y salimos del bucle
            nGeneradas.append(n)
            return n
###################################################################
#Funciones principales                                            #
###################################################################

########################### Ejercicio 1 ###########################
#Función primosolostra. 
def primosolostra(rango1, rango2, iter): 
    cont = 0 # contador de números generados
    numeros = 5 # números que se van a generar
    nGeneradas = [] # lista para ver qué números se han creado ya

    # Probar x valores aleatorios del rango
    while cont < numeros :
        # Se genera un valor aleatorio de n dentro del rango dado, para comprobar si es primo

        n = generarN(rango1, rango2, nGeneradas) # Generar un valor n aleatorio (que no haya sido ya generado)

        # Medición del tiempo de inicio del rango
        start_time = time.perf_counter() # Función de la biblioteca time para medir el tiempo de forma precisa.
         
        if n == 2:
            esPrimoOlostra = True

        # Asegurarse que n sea impar
        if n % 2 == 0:
            esPrimoOlostra = False
        
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
        
        # Iteramos varias veces para probar el valor de n.
        for _ in range(iter): # _ porque el valor no se va a usar explicitamente en el código

            a = random.randint(2, n-1) # Generar una a aleatoria entre 2 y n-1
            u=pow(a, (n-1)//2, n) # Calcular a ^ ((n-1)/2) mod(n)
            v = simbolo_legendre(a, n)

            if u != v % n: 
                esPrimoOlostra = False
        
        esPrimoOlostra = True
        
        # Medición del tiempo de finalización del rango
        end_time = time.perf_counter() # Función de la biblioteca time para medir el tiempo de forma precisa.
        elapsed_time = end_time - start_time # Calculamos el tiempo restando el final y el inicial.

        print(f"\nTiempo requerido en el primosolostra: {elapsed_time:.4f} segundos")  # Imprimimos el valor

        # Si pasa el test
        if esPrimoOlostra:
            print(f"{n} pasó el test de Solovay-Strassen")
            prob=(1/2)**iter # Probabilidad de que sea pseudo-primo
            print(f"Probabilidad de que sea pseudo-primo: {prob}\n")
        else:
            print(f"{n} NO pasó el test de Solovay-Strassen\n")

        cont += 1


#Función primoMillerRabin
def primoMillerRabin(rango1, rango2, iter): 
    
    cont = 0 # contador de números generados
    numeros = 5 # números que se van a generar
    nGeneradas = [] # lista para ver qué números se han creado ya

    # Probar x valores aleatorios del rango
    while cont < numeros :
        # Se genera un valor aleatorio de n dentro del rango dado, para comprobar si es primo

        n = generarN(rango1, rango2, nGeneradas) # Generar un valor n aleatorio (que no haya sido ya generado)

        # Medición del tiempo de inicio del rango
        start_time = time.perf_counter() # Función de la biblioteca time para medir el tiempo de forma precisa.

        if n == 2: 
            return True
        
        if n % 2 == 0: # n debe ser impar
            return False

        s = 0
        d = n -1 

        while d % 2 == 0: 
            d //= 2
            s += 1 

        # Iteramos varias veces para probar el valor de n.
        for _ in range(iter): # _ porque el valor no se va a usar explicitamente en el código
            a = random.randint(2, n-1) # Generar una a aleatoria entre 1 y n-1

            esPrimo = False

            if pow(a, d, n) == 1: # Si a^d mod n es igual que 1, ha pasado este test
                esPrimo = True
            else: 
                for r in range(s): # Comprobamos para algún valor de r<s
                    if pow(a, 2**r * d, n) == n-1: # Si a^(2^r * d) mod n es igual que n-1, ha pasado este test
                        esPrimo = True
                        break
    
        end_time = time.perf_counter() 
        elapsed_time = end_time - start_time 

        print(f"Tiempo requerido en el primoMillerRabin: {elapsed_time:.4f} segundos")  # Imprimimos el valor

        # Si pasa el test
        if esPrimo:
            print(f"{n} pasó el test de Miller Rabin")
            prob=(1/4)**iter # Probabilidad de que sea pseudo-primo
            print(f"Probabilidad de que sea pseudo-primo: {prob}\n")
            #return n

        else:
            print(f"{n} NO pasó el test de Miller Rabin\n")

        cont += 1

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
            print("Se probaran si 5 valores aleatorios del rango que introduzcas son primos")
            rango1 = obtener_numero_entero("Introduce un valor para el primer valor del rango (que no sea 1): ")

            if rango1 != 1: 
                rango2 = obtener_numero_entero("Introduce un valor para el segundo valor del rango (que sea mayor que el primer valor): ")
                if rango1 < rango2:
                    iter = obtener_numero_entero("Introduce un valor para el número de iteraciones: ")
                    primosolostra(rango1, rango2, iter)
                    primoMillerRabin(rango1, rango2, iter)
                else: 
                    print("El primer valor debe ser más pequeño que el segundo\n")
            else: 
                print("El primer valor del rango no debe ser 1\n")

        elif op == 2:
            print("Saliendo del programa.\n")
            break

        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 4.\n")

menu()