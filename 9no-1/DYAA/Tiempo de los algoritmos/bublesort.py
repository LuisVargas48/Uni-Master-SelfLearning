#Luis Alberto Vargas Glez. 
#19012140. 
#Diseño y análisis de algoritmos. 

import time 
import random

inicio = time.time()

#codigo a medir 
time.sleep(1)
def burbuja2(arreglo):
    contador = 0
    ordenado = False
    i = 0
    while i < len(arreglo) and not ordenado:
        ordenado = True
        for j in range(len(arreglo)-i-1):
            if arreglo[j] > arreglo[j+1]:
                arreglo[j],arreglo[j+1] = arreglo[j+1],arreglo[j]
                ordenado = False
            contador += 1
        i += 1
    print("Contador =",contador)
    return arreglo


arr = [random.randint(1,10000) for x in range(10000)]

#---------

fin=time.time()
print(fin - inicio)
#print(arr)
#print(burbuja2(arr))