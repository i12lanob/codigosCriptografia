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

#Función seleccion_e
def seleccion_e(phi, e_opcion):
   
    if e_opcion == "fermat":
        e = 65537  # Primo de Fermat

        if algeucl(e, phi) != 1:
            print("e=65537 no es coprimo con φ(n). Selecciona otra opción.")

    elif e_opcion == "aleatorio":
        while True:
            e = random.randint(2, phi - 1) # Valor aleatorio entre 2 y phi - 1
            if algeucl(e, phi) == 1:
                break
    elif isinstance(e_opcion, int):
        e = e_opcion

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
def keygeneration(p, q):

    if algeucl(p,q)==1:
    
        # Calcula n y φ(n)
        n = p * q
        phi = (p - 1) * (q - 1)

        print("Opciones para e:")
        print("1. Primo de Fermat (65537)")
        print("2. Valor aleatorio")
        print("3. Introducir un valor específico")
        e_opcion = int(input("Elige una opción para e (1, 2 o 3): "))

        if e_opcion == 1:
            e_opcion = "fermat"
        elif e_opcion == 2:
            e_opcion = "aleatorio"
        elif e_opcion == 3:
            e_opcion = int(input("Introduce el valor específico para e: "))
                    
        else:
            print("Opción no válida para e.")
        # Selección de e usando la función auxiliar   
        e = seleccion_e(phi, e_opcion)
        
        # Calcula d (inverso modular de e módulo φ(n))
        d = invmod(e, phi)

        # Claves pública y privada
        clave_publica = (n, e)
        clave_privada = (n, d)
    else:
        print("Introduzca números primos")
    return clave_publica, clave_privada

########################### Ejercicio 3 ###########################
#Función textoACifras
def TextoACifras(texto):
    alfabeto = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
    cifras = []
    
    for letra in texto.upper():  # Convertir todo el texto a mayúsculas
        if letra in alfabeto:  # Considerar solo letras de A a Z y Ñ
            numero = alfabeto.index(letra)  # Obtener el índice de la letra.Devuelve la posición del alfabeto A=00,B=01...Z=26
            cifras.append(f'{numero:02d}')  # Convertir a cadena de 2 cifras (00, 01, ..., 26)
    
    return cifras

#Función CifrasATexto
def CifrasATexto(cifras):
    # Diccionario que mapea números a letras en Z27 (A-Z + Ñ)
    alfabeto = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
    texto = ''
    
    for cifra in cifras:
        numero = int(cifra)
        if 0 <= numero <= 26:  # Asegurarse de que el número está en el rango válido
            texto += alfabeto[numero]  # Convertir el número de vuelta a una letra
        else:
            texto += '?'  # Si hay un valor fuera de rango, reemplazar por un signo de interrogación
    
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
    n,e = clave_publica
    # Asegúrate de que cada bloque sea un entero
    bloques_cifrados = []
    for bloque in bloques:
        # Convertir bloque a entero si no lo es
        if isinstance(bloque, str):
            bloque = int(bloque)
        # Aplicar cifrado RSA: C = M^e % n
        c = pow(bloque, e, n)
        bloques_cifrados.append(c)
    return bloques_cifrados

#Función rsadecipher
def rsadecipher(bloques_cifrados, clave_privada):
    n,d= clave_privada
    bloques_descifrados = []
    
    # Descifrar cada bloque usando la fórmula M_i = C_i^d % n
    for bloque_cifrado in bloques_cifrados:
        m = pow(bloque_cifrado, d, n)  # Descifrado con la fórmula C^d % n
        bloques_descifrados.append(m)  # Añadir el bloque descifrado
    
    return bloques_descifrados
########################### Ejercicio 6 ###########################
#Función rsaciphertext
def rsaciphertext(texto, clave_publica):
    
    # Convertir el texto en bloques numéricos (ASCII)
    bloque = TextoACifras(texto)  # Convertir cada carácter a cifras numéricas
       
    # Cifrar los bloques usando la función rsacipher
    bloques_cifrados = rsacipher(bloque, clave_publica)
    return bloques_cifrados

#Función rsadeciphertext
def rsadeciphertext(bloques_cifrados, clave_privada):
    # Descifrar los bloques usando la función rsadecipher
    bloques_descifrados = rsadecipher(bloques_cifrados, clave_privada)

    # Convertir los bloques descifrados de vuelta a texto
    texto = ""
    for bloque in bloques_descifrados:
        texto += CifrasATexto([str(bloque)]) 
    return texto
########################### Ejercicio 7 ###########################
#Función rsaciphertextsign
def rsaciphertextsign(clave_publicab, clave_privadaa, texto, firma):
    # Primer paso, cifrar con la clave pública de b el texto y la firma 
    cadena = ''.join([texto, firma]) # Concatenar la firma y el texto en una sola cadena
    textoFirma_cifrados = rsaciphertext(cadena, clave_publicab) # Primer paso completado, tenemos cifrada el texto y la firma

    # Segundo paso, cifrar la firma primero con la clave privada de a y luego con la pública de b
    firma_cifrada = rsaciphertext(firma, clave_privadaa) # Primero cifro con clave privada
    firma_cifrada = rsaciphertext(firma, clave_publicab) # Después cifro con clave pública 
   
    return textoFirma_cifrados, firma_cifrada
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
       # Llamar a la generación de claves usando la función `keygeneration`
            print("Posibles números primos para utilizar:") 
            print("5, 17, 61, 103, 229, 419, 601, 887, 1201, 1697, 2083, 2593, 3253, 4001, 4999, 5647, 7001, 8089, 9437, 9929")
            p = int(input("Introduce el primer número primo (p): "))
            q = int(input("Introduce el segundo número primo (q): "))
            
            clave_publica, clave_privada = keygeneration(p, q)
            if clave_publica and clave_privada:
                print(f"\nCLAVE PÚBLICA: {clave_publica}")
                print(f"CLAVE PRIVADA: {clave_privada}\n")
            else:
                print("Error en la generación de claves. Por favor, asegúrate de introducir valores válidos.\n")

        elif op == 3: 
            cadena = input("Introduce una cadena a dividir: ")
            cadena_num=TextoACifras(cadena)
            n = obtener_numero_entero("Introduce un valor para dividir la cadena: ")

            resultado = preparenumcipher(cadena_num, n)
            print(f"La cadena transformada y dividida queda como {resultado}\n")

            print(f"La cadena transformada y dividida queda como {preparetextdecipher(resultado)}\n")
        elif op == 4:  # Opción añadida para Cifrado y Descifrado RSA
            print("\nCifrado y Descifrado RSA")
            mensaje = ["22", "08", "04", "18", "13", "04", "19"]  # Mensaje original (representado como una lista de cadenas numéricas)
            clave_publica = (3233, 17)  # Ejemplo de clave pública (n=3233, e=17)
            clave_privada = (3233, 2753)
            # Convertir el mensaje a bloques de números
            bloques_numericos = preparenumcipher(mensaje, 2)  # Usamos bloques de tamaño 2
            print(f"Bloques numéricos: {bloques_numericos}")

            # Cifrar el mensaje
            bloques_cifrados = rsacipher(bloques_numericos, clave_publica)
            print(f"Mensaje cifrado: {bloques_cifrados}")
            
            bloques_descifrados = rsadecipher(bloques_cifrados, clave_privada)
            print(f"Mensaje descifrado: {bloques_descifrados}")
            fin=CifrasATexto(bloques_descifrados)
            print(f"{fin}")
        elif op == 5:
            clave_publica = (7073, 2753)  # Ejemplo de clave pública (n, e)
            clave_privada = (7073, 11)    # Ejemplo de clave privada (n, d)

            # Texto a cifrar
            texto = "HOLA"

            # Cifrar el texto con la clave pública
            bloques_cifrados = rsaciphertext(texto, clave_publica)
            print("Texto cifrado:", bloques_cifrados)

            # Descifrar los bloques con la clave privada
            texto_descifrado = rsadeciphertext(bloques_cifrados, clave_privada) 
            print("Texto descifrado:", texto_descifrado)
        elif op == 6:
            print("Saliendo del programa.\n")
            break

        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 4.\n")

menu()