###################################################################
#Práctica 3: Cifrado por Mochilas y Mochilas trampa               #
###################################################################
#Blanca Lara Notario                                              #
#Rafael Bueno Espinosa                                            #
#Francisco Bueno Espinosa                                         #
###################################################################

import re
import math

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

#Función NumberToBinario. Dado un vector con los números en código ASCII se pasaran a binarios. 
def NumberToBinario(texto_numerico):
    vector_binario = []

    for num in texto_numerico:
        #Transformar a binario. En este caso un número binario (b) de 8 caracteres y rellenar con 0 (a la izquierda)
        binario = format(num, '08b') #format permite especificar el formato. 
        vector_binario.append(binario)
        
    return vector_binario

#Función comprobar_valor_m. Comprueba si el valor de m es mayor que todos los valores del vector s. 
def comprobar_valor_m(m, s): 

    if m > 2*s[len(s)-1]: # Si el valor de m es m>2Sn (siendo Sn el último valor del vector)
        return 1
    
    else: 
        return -1
    
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
    for i in range(len(vector_fila)): # Recorre cada elemento del vector_fila
        if vector_fila[i] < 0 or not isinstance(vector_fila[i], int): # Verifica dos condiciones:
        # 1. Si el elemento en la posición i es negativo (vector_fila[i] < 0)
        # 2. Si el elemento no es un número entero (not isinstance(vector_fila[i], int))
            return -1 # Si alguna de las dos condiciones es verdadera, retorna -1
       
    for i in range (len(vector_fila)): 
        suma += vector_fila[i]
        if suma < vector_fila[i+1]: # Si suma < vector_fila[i+1], es no supercreciente
            return 0
        
    return 1 # Es una mochila super creciente si el valor de la suma < vector_fila[i+1]

#Función knapsacksol. Hecho de forma recursiva por si la mochila es no supercreciente.
def knapsacksol(s, m, j):
    # Caso base: si m es 0, significa que hemos encontrado una combinación
    if m == 0:
        return 0  # V es objetivo de s
    
    # Si hemos recorrido todos los elementos de s y m no es 0, no hemos encontrado solución
    if j < 0 or m < 0:
        return -1  # No es objetivo de s
    
    # Opción 1: Incluimos el elemento s[j] y restamos su valor de m
    # Si m >= s[j]
    if knapsacksol(s, m - s[j], j - 1) == 0:
        return 0  # Si en alguna de las opciones conseguimos m = 0, devolvemos 0
    
    # Opción 2: No incluimos el elemento s[j] y seguimos con el siguiente
    # Si m < s[j]
    return knapsacksol(s, m, j - 1)

#Función knapsackcipher.
def knapsackcipher(vector, texto): 
    texto_numerico = TextToNumber(texto) # Convertir el texto a codigo ASCII

    binario = NumberToBinario(texto_numerico) # Convertir ASCII a binario

    # Unir todos los binarios en una sola cadena
    cadena_binaria = ''.join(binario) # Unir los valores binarios en una única cadena

    cadena = []
    # range (start, stop, step)
    # Primer valor--> valor de inicio. 
    # Segundo valor--> límite superior. 
    # Tercer valor--> tamaño del paso.
    for i in range(0, len(cadena_binaria), len(vector)): 
        cadena_dividida = [] # Para dividir la cadena binaria en bloques según el tamaño del vector
        
        # Llenar el bloque hasta alcanzar el tamaño del vector
        for j in range(len(vector)):
            if i + j < len(cadena_binaria):  # Asegurarse de no exceder la longitud del vector
                cadena_dividida.append(cadena_binaria[i + j])
            else:
                cadena_dividida.append('1')  # Si el bloque es más pequeño rellenar con 1
        
        cadena.append(''.join(cadena_dividida)) # Para que en el vector no quede como ['0', '1', '1', '0'], sino como ['0110']

    resultado = []

    for i in cadena: # Recorrer la cadena generada con los números binarios divididos en bloques
        suma = 0
        for j,  bit in enumerate(i): # enumerate da tanto el índice como el valor 
            if bit == '1': # Si el valor del bit es 1 sumamos el valor
                suma += vector[j]

        resultado.append(suma)

    return resultado

#Función knapsackdecipher.
def knapsackdecipher(clave, texto_cifrado):
    # Paso 1: Convertir cada número en `texto_cifrado` a su representación binaria usando la clave
    texto_binario = []
    
    for valor in texto_cifrado:
        binario = ""
        suma_actual = valor
        
        # Recorrer la clave en reversa para descomponer el valor
        for peso in reversed(clave): #  Invierte el orden de una lista o un vector
            if suma_actual >= peso:
                binario = '1' + binario # Si la suma es mayor que el propio valor se pone un 1.
                suma_actual -= peso
            else:
                binario = '0' + binario # Si la suma es menor que el propio valor se pone un 0
        
        texto_binario.append(binario)
    
    # Unimos todos los binarios en una sola cadena
    cadena_binaria = ''.join(texto_binario)
    
    # Agrupamos en bloques de 8 bits y convertir a texto
    texto_plano = ""
    longitud = len(cadena_binaria)
    # Usamos un bucle while para recorrer la cadena
    i = 0
    while i < longitud:
        bloque = ""
        
        # Crear un bloque de 8 bits manualmente
        for j in range(8):
            if i < longitud:  # Asegurarnos de no salir del rango
                bloque += cadena_binaria[i]
                i += 1
        
        # Asegurarnos de que el bloque tiene 8 bits
        if len(bloque) == 8:
            # Convertir el bloque de binario a decimal y luego a carácter
            cadena=(int(bloque,2))
            texto_plano += ascii2letter(cadena)
    
    return texto_plano

########################### Ejercicio 3 ###########################
#Función commonfactors.
def commonfactors(w, s):
    # Función para encontrar los factores primos de un número
    def get_factors(n):
        factors = [] #Se crea una lista vacía para almacenar los factores primos de n
        # Comprobamos si 2 es un factor
        while n % 2 == 0: #Verificamos si el número n es divisible por 2 (único número primo par)
            factors.append(2) #Se añade a la lista factors
            n //= 2 #Se divide entre dos usando la división entera
        # Comprobamos factores impares a partir de 3
        for i in range(3, n + 1, 2): #Se itera desde 3 hasta n, en números impares (a 3 se suma 2 y así sucesivamente)
            while n % i == 0: #Verificamos si el número n es divisible por 3 y sus sucesivos impares
                factors.append(i) 
                n //= i #Se divide 𝑛 n por 𝑖 i hasta que ya no sea divisible.
        # Si queda un número primo mayor que 2, lo añadimos
        if n > 2: #Si 𝑛 n sigue siendo mayor que 2 ,𝑛 n es un número primo.
            factors.append(n)
        return factors
    
    # Obtenemos los factores de w
    w_factors = get_factors(w)
    
    # Recorremos la lista s
    for number in s:
        # Obtenemos los factores del número en s
        s_factors = get_factors(number)
        
        # Verificamos si hay factores comunes
        for factor in w_factors:
            if factor in s_factors:
                return True  # Si hay un factor común, devolvemos True
    
    return False  # Si no encontramos factores comunes, devolvemos False

#Función knapsackpublicandprivate.
def knapsackpublicandprivate(s, m, w): 

    b = []

    for i in range(len(s)): 
        b.append((w * s[i]) % m) # Crear la mochila trampa bi=w*ai mod m

    print("Clave privada: ", s) 
    print("Clave pública: ", b)

    return b

#Función knapsackdeciphermh.


########################### Ejercicio 4 ###########################

############################## Menú ###############################
print("1. Cadena a ASCII")
print("2. ASCII a letra")
print("3. Comprobar si es mochila, supercreciente o no supercreciente")
print ("4. V es objetivo de s")
print ("5. Cifrado y descifrado por mochilas")
print ("6. Factores en común")
print("7. Cifrado con mochilas trampa")
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

if op == 4: 
    s = [1, 6, 3, 27, 13]
    #v = 19
    v = 21
    j = len(s) - 1
    if knapsacksol(s, v, j) == 0: # Si el valor que devuelve la función es 0 es que v es un valor objetivo de s
        print("V es objetivo de s\n")
    
    else: # Si no es que v no es un valor objetivo de s
        print("V no es objetivo de s\n")

if op == 5:
    s = [1, 4, 6, 13, 25]
    texto=input("Introduce un texto a cifrar: ")
    cadena=knapsackcipher(s, texto)
    print("El texto cifrado es ", cadena, "\n")
    print("El texto descifrado es ",knapsackdecipher(s, cadena)) 

if op == 6:
    w = 30
    s = [11, 7, 14]
    print(commonfactors(w, s))  # Esto debería devolver True porque 30 y 15 comparten el factor primo 3.

if op == 7:
    s = [3, 5, 11, 21]
    m = obtener_numero_entero("Introduce el valor de m: ")
    if comprobar_valor_m(m, s): 
        w = obtener_numero_entero("Introduce el valor de w: ")
        if algeucl(m, w)==1 and commonfactors(w, s)==False: 
            knapsackpublicandprivate(s, m, w)
        else: 
            print("m y w deben de ser coprimos y m no debe tener primos comunes con s")
    else: 
        print("El valor de m debe ser vayor que la suam de los valores de la mochila\n")