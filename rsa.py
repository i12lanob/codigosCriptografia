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

#Función algeucl. 
def algeucl(a, b): 
    """Calcula el MCD usando el Algoritmo de Euclides."""
    while b != 0:
        temp = b  # Crear una variable temporal para guardar b
        b = a % b  # Actualizar b con el resto de a y b (nuevo divisor)
        a = temp  # Actualizar a (nuevo dividendo)
    return a

#Función invmod.
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

#Función comprobar_primo. Comprobar si un número es primo.                                           
def comprobar_primo(n):
    if n <= 1:
        return False  # Los números <= 1 no son primos
    for i in range(2, n):
        if n % i == 0:  # Si es divisible por cualquier número, no es primo
            return False
    return True

#Función seleccion_e
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
         
        esPrimoOlostra = True

        if n == 2:
            esPrimoOlostra = True

        # Asegurarse que n sea impar
        elif n % 2 == 0:
            esPrimoOlostra = False
        
        else: 
            # Iteramos varias veces para probar el valor de n.
            for _ in range(iter): # _ porque el valor no se va a usar explicitamente en el código

                a = random.randint(2, n-1) # Generar una a aleatoria entre 2 y n-1
                u=pow(a, (n-1)//2, n) # Calcular a ^ ((n-1)/2) mod(n)
                v = simbolo_legendre(a, n)

                if u != v % n: 
                    esPrimoOlostra = False
        
        # Medición del tiempo de finalización del rango
        end_time = time.perf_counter() # Función de la biblioteca time para medir el tiempo de forma precisa.
        elapsed_time = end_time - start_time # Calculamos el tiempo restando el final y el inicial.


        # Si pasa el test
        if esPrimoOlostra:
            print(f"\n{n} pasó el test de Solovay-Strassen")
            prob=(1/2)**iter # Probabilidad de que sea pseudo-primo
            print(f"Probabilidad de que sea pseudo-primo: {prob}")
        else:
            print(f"\n{n} NO pasó el test de Solovay-Strassen")
        
        print(f"Tiempo requerido en el primosolostra: {elapsed_time:.4f} segundos\n")  # Imprimimos el valor

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
            esPrimo = True
        
        elif n % 2 == 0: # n debe ser impar
            esPrimo = False

        else:
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

        # Si pasa el test
        if esPrimo:
            print(f"\n{n} pasó el test de Miller Rabin")
            prob=(1/4)**iter # Probabilidad de que sea pseudo-primo
            print(f"Probabilidad de que sea pseudo-primo: {prob}")
            #return n

        else:
            print(f"\n{n} NO pasó el test de Miller Rabin")

        print(f"Tiempo requerido en el primoMillerRabin: {elapsed_time:.4f} segundos\n")  # Imprimimos el valor

        cont += 1

########################### Ejercicio 2 ###########################
#Función keygeneration
def keygeneration(p, q, opcion_e):

    if not (comprobar_primo(p) and comprobar_primo(q)):
        print("Ambos números deben ser primos. Por favor, verifica los valores de p y q.")
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

#Función CifrasATexto
def CifrasATexto(cadena_numerica):
    texto = ""
    # Recorrer la cadena tomando dos caracteres a la vez
    i = 0
    while i< len(cadena_numerica):
        # Tomar dos caracteres consecutivos
        cifra = cadena_numerica[i] + cadena_numerica[i + 1]
        num = int(cifra)  # Convertir a número
        if 0 <= num <= 25:  # Si está en el rango 0-25
            texto += chr(num + ord('A'))  # Convertir a letra
        i += 2  # Avanzar al siguiente par de caracteres
    return texto
    
########################### Ejercicio 4 ###########################
#Función preparenumcipher 
def preparenumcipher(cad_num, n): 

    cadena = ''.join(cad_num) # Unir los valores en una única cadena
    resultado = []

    for i in range(0, len(cadena), n): 
        cadena_dividida = [] # Para dividir la cadena en bloques de tamaño n
        
        for j in range(n):
            if i + j < len(cadena):  # Asegurarse de no exceder la longitud del vector
                cadena_dividida.append(cadena[i + j])
            else:
                faltan = n - len(cadena_dividida) # Ver cuántos caracteres quedan
                if faltan == 1:  # Si falta un carácter, rellenar con '0'
                    cadena_dividida.append('0')
                elif faltan > 1:  # Si faltan más de un carácter, rellenar con '30'
                    while faltan > 1:  # Rellenar bloques de '30'
                        cadena_dividida.extend(['3', '0'])
                        faltan -= 2
                    if faltan == 1:  # Si aún falta un carácter, añadir '0'
                        cadena_dividida.append('0')
        
        resultado.append(''.join(cadena_dividida)) # Para que en el vector no quede como ['0', '0', '0', '1'], sino como ['0001']

    return resultado

def preparetextdecipher(cad_num):
    cadena = ''.join(cad_num)  # Unir los valores en una única cadena
    resultado = []
    i = 0

    while i < len(cadena):  # Recorrer la cadena completa
        # Revisar si estamos en los últimos bloques y necesitamos ajustar
        if i + 1 < len(cadena):  # Si aún hay espacio para leer dos caracteres
            if cadena[i] == '3' and cadena[i + 1] == '0':  # Detectar relleno con '30'
                # Si encontramos relleno, saltamos estos dos caracteres
                i += 2
                continue
        if i == len(cadena) - 1 and len(cadena) % 2 != 0: # Si estamos ya al final y la cadena es impar la saltamos (porque al ser impar está rellena de un 0)
            if cadena[i] == '0':
                break

        # Agregar el carácter si no es relleno
        resultado.append(cadena[i])
        i += 1

    return ''.join(resultado)  # Devolver la cadena sin rellenos

########################### Ejercicio 5 ###########################
#Función rsacipher
def rsacipher(bloques, clave_publica):
    n, e = clave_publica
    bloques_cifrados = []
    
    # Cifrar cada bloque usando la fórmula C_i = M_i^e % n
    for bloque in bloques:
        c = pow(bloque, e, n)  # Cifrado con la fórmula M^e % n
        bloques_cifrados.append(c)  # Añadir el bloque cifrado
    
    return bloques_cifrados

# Función de descifrado RSA
def rsadecipher(bloques_cifrados, clave_privada):
    n, d = clave_privada
    bloques_descifrados = []
    
    # Descifrar cada bloque usando la fórmula M_i = C_i^d % n
    for bloque_cifrado in bloques_cifrados:
        m = pow(bloque_cifrado, d, n)  # Descifrado con la fórmula C^d % n
        bloques_descifrados.append(m)  # Añadir el bloque descifrado
    
    return bloques_descifrados
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
        print("2. Prueba de claves")
        print("3. Preparar cadena numerica")
        print("4. Cifrado y descifrado RSA")
        print("5. Salir")
        op = int(input("Elige una de las opciones: "))
        print("\n")

        if op == 1:
            print("Se probaran si 5 valores aleatorios del rango que introduzcas son primos")
            rango1 = obtener_numero_entero("Introduce un valor para el primer valor del rango (que no sea 1): ")

            if rango1 != 1: 
                rango2 = obtener_numero_entero("Introduce un valor para el segundo valor del rango (que sea mayor que el primer valor): ")
                if rango1 < rango2:
                    iter = obtener_numero_entero("Introduce un valor para el número de iteraciones: ")

                    print("\n\n-----Test de Solovay-Strassen-----")
                    primosolostra(rango1, rango2, iter)

                    print("\n\n-----Test Miller Rabin-----")
                    primoMillerRabin(rango1, rango2, iter)
                
                else: 
                    print("El primer valor debe ser más pequeño que el segundo\n")
            else: 
                print("El primer valor del rango no debe ser 1\n")
        
        elif op == 2:
            # Pedir al usuario los valores de p, q y la opción para e
            print("Posibles números primos para utilizar:") 
            print("5, 17, 61, 103, 229, 419, 601, 887, 1201, 1697, 2083, 2593, 3253, 4001, 4999, 5647, 7001, 8089, 9437, 9929")
            p = int(input("Introduce el primer número primo (p): "))
            q = int(input("Introduce el segundo número primo (q): "))

            if not (comprobar_primo(p) and comprobar_primo(q)) or p == q:
                print("Por favor, ingresa nuevamente valores válidos para p y q.")
                continue# Si no son válidos, volvemos a pedir los números
            
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
            cadena = input("Introduce una cadena a dividir: ")
            cadena_num=TextoACifras(cadena)
            n = obtener_numero_entero("Introduce un valor para dividir la cadena: ")

            resultado = preparenumcipher(cadena_num, n)
            print(f"La cadena transformada y dividida queda como {resultado}\n")

            print(f"La cadena transformada y dividida queda como {preparetextdecipher(resultado)}\n")
        elif op == 4:  # Opción añadida para Cifrado y Descifrado RSA
            print("\nCifrado y Descifrado RSA")
            n = int(input("Introduce el valor de n (módulo de la clave): "))
            e = int(input("Introduce el valor de e (exponente público): "))
            d = int(input("Introduce el valor de d (exponente privado): "))

            # Generación de claves RSA (para este ejemplo simple asumimos que se dan directamente)
            clave_publica = (n, e)
            clave_privada = (n, d)

            # El usuario ingresa el mensaje que quiere cifrar
            mensaje = input("Introduce el mensaje que deseas cifrar: ")
            mensaje_num = TextoACifras(mensaje)  # Convertir el texto a números

            # Preparar los bloques numéricos
            n_value = obtener_numero_entero("Introduce el tamaño de los bloques: ")
            bloques = preparenumcipher(mensaje_num, n_value)

            # Cifrado de bloques con la clave pública
            print("\nCifrando el mensaje...")
            bloques_cifrados = rsacipher(bloques, clave_publica)
            print(f"Mensaje cifrado: {bloques_cifrados}")

            # Descifrado de bloques con la clave privada
            print("\nDescifrando el mensaje...")
            bloques_descifrados = rsadecipher(bloques_cifrados, clave_privada)
            mensaje_final = CifrasATexto(bloques_descifrados)
            print("Mensaje descifrado:", mensaje_final)
         

        elif op == 5:
            print("Saliendo del programa.\n")
            break

        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 4.\n")

menu()