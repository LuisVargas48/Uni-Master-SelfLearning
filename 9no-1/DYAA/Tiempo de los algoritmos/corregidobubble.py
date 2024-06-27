import time 
import random


#codigo a medir 
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
    return arreglo

#---------

#peor caso: 
arreglo1=[x for x in range(1000)]
inicio = time.time()
arreglo1.reverse()
burbuja2(arreglo1)
fin=time.time()
print("tiempo peor", fin - inicio, " segundos")



#caso promedio: 
#arreglo2=[random.randint(1,1000) for x in range(1000)]
#inicio2=time.time()
#burbuja2(arreglo2)
#fin2=time.time()
#print("tiempo promedio", fin2 - inicio2, " segundos")



#caso mejor
#arreglo3=[random.randint(1,1000) for x in range(1000)]
#inicio3=time.time()
#burbuja2(arreglo3)
#fin3=time.time()
#print("tiempo mejor", fin3 - inicio3, " segundos")