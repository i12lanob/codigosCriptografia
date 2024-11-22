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
#Funciones útiles   
# 
# import random

def algeucl(a, b): 
    """Calcula el MCD usando el Algoritmo de Euclides."""
    while b != 0:
        temp = b  # Crear una variable temporal para guardar b
        b = a % b  # Actualizar b con el resto de a y b (nuevo divisor)
        a = temp  # Actualizar a (nuevo dividendo)
    return a

def invmod(p, n):
    """Calcula el inverso modular de p módulo n."""
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
            return "Los números no son coprimos, no se puede calcular el inverso.\n"
    else:
        return "Los números deben ser naturales.\n"
                                                  

####################################################################
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
def seleccion_e(phi, opcion_e):
   
    if opcion_e == "fermat":
        e = 65537  # Primo de Fermat

        if algeucl(e, phi) != 1:
            print("e=65537 no es coprimo con φ(n). Selecciona otra opción.")

    elif opcion_e == "aleatorio":
        while True:
            e = random.randint(2, phi - 1) # Valor aleatorio entre 2 y phi - 1
            if algeucl(e, phi) == 1:
                break
    elif isinstance(opcion_e, int):
        e = opcion_e

        if algeucl(e, phi) != 1:
            print("El valor dado de e no es coprimo con φ(n).")
    else:
        print("Opción de e no válida. Usa 'fermat', 'aleatorio' o un entero.")
    return e

def keygeneration(p, q, opcion_e):
    if not (p > 1 and q > 1):
        print("Ambos números deben ser mayores que 1.")
    if p == q:
        print("Los números primos p y q deben ser distintos.")
    
    # Calcula n y φ(n)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Selección de e usando la función auxiliar
    e = seleccion_e(phi, opcion_e)
    
    # Calcula d (inverso modular de e módulo φ(n))
    d = invmod(e, phi)

    # Claves pública y privada
    clave_publica = (n, e)
    clave_privada = (n, d)
    
    return clave_publica, clave_privada
########################### Ejercicio 3 ###########################
#Función textoACifras
def TextoACifras(texto):
    # Convertir el texto a mayúsculas
    texto = texto.upper()

    # Crear una lista vacía para almacenar los números
    cadena_numerica = []

    # Iterar sobre cada caracter en el texto
    for char in texto:
        if 'A' <= char <= 'Z':  # Verificar si el caracter es una letra
            # Convertir la letra a un número de dos cifras (A=00, B=01, ..., Z=25)
            numero = ord(char) - ord('A')
            cadena_numerica.append(f"{numero:02d}")  # Asegura que el número tenga dos cifras
        
    
    return cadena_numerica


def CifrasATexto(cadena_numerica):
    texto=""
    # Iterar sobre cada cifra en la lista
    for cifra in cadena_numerica:
        num = int(cifra) 
        if 0 <= num <= 25:  # Si la cifra está entre 0 y 25, lo mapeamos a una letra
            texto += chr(num + ord('A'))  # Convertimos el número a la letra correspondiente
    
    return texto
########################### Ejercicio 4 ###########################
#Función preparenumcipher 
#def preparenumcipher(cadena_numerica, n):
   # n=5
    
   # for
        






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
        print("2.Prueba de claves")
        print("3. TextoACifras")
        print("4.CifrasATexto")
        print("5.Practicando")
        op = input("Elige una de las opciones: ")
        print("\n")

        op = int(op)

        if op == 1:
            rango = obtener_numero_entero("Introduce un valor para el rango: ")
            iter = obtener_numero_entero("Introduce un valor para el número de iteraciones: ")
            testPrimos(rango, iter)
        elif op == 2:
                # Pedir al usuario los valores de p, q y la opción para e
                p = int(input("Introduce el primer número primo (p): "))
                q = int(input("Introduce el segundo número primo (q): "))
                print("Opciones para e:")
                print("1. Primo de Fermat (65537)")
                print("2. Valor aleatorio")
                print("3. Introducir un valor específico")
                e_opcion = int(input("Elige una opción para e (1, 2 o 3): "))

                if e_opcion == 1:
                    opcion_e = "fermat"
                elif e_opcion == 2:
                    opcion_e = "aleatorio"
                elif e_opcion == 3:
                    opcion_e = int(input("Introduce el valor específico para e: "))
                    
                else:
                    print("Opción no válida para e.")
                    
                clave_publica, clave_privada = keygeneration(p, q, opcion_e)
                print(f"\nCLAVE PÚBLICA: {clave_publica}")
                print(f"CLAVE PRIVADA: {clave_privada}\n")
        elif op == 3:
                texto = input("Introduce el texto a convertir a cifras: ")
                numeros = TextoACifras(texto)
                print("Texto convertido a cifras:", numeros)
        elif op == 4:
                cadena = [7, 14, 11, 0, 12, 20, 13, 3, 14]
                texto = CifrasATexto(cadena)
                print("Cifras convertidas a texto:", texto)

        #elif op == 5:
         #       cadena = [7, 14, 11, 0, 12, 20, 13, 3, 14]
         #       cadena_numerica=preparenumcipher(cadena)
               
        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 4.\n")

menu()