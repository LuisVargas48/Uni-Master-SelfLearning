#Luis Alberto Vargas González. 
#19012140
#Diseño y análisis de algoritmos. 


import time
import random



#codigo a medir.
def quick_sort(sequence):
    length = len(sequence)
    if length < 1:
        return sequence
    else:
        pivot = sequence.pop()

    items_greater = []
    items_lower = []

    for item in sequence:
        if item > pivot:
            items_greater.append(item)

        else:
            items_lower.append(item)

    return quick_sort(items_lower) + [pivot] + quick_sort(items_greater)


lista=[random.randint(1,10000) for x in range(10000)]


#---------

#peor caso: 
arreglo1=[x for x in range(1000000000000)]
inicio = time.time()
arreglo1.reverse()
quick_sort(arreglo1)
fin=time.time()
print("tiempo peor", fin - inicio, " segundos")



#caso promedio: 
#arreglo2=[random.randint(1,1000) for x in range(1000)]
#inicio2=time.time()
#insercion(arreglo2)
#fin2=time.time()
#print("tiempo promedio", fin2 - inicio2, " segundos")



#caso mejor
#arreglo3=[random.randint(1,1000) for x in range(1000)]
#inicio3=time.time()
#insercion(arreglo3)
#fin3=time.time()
#print("tiempo mejor", fin3 - inicio3, " segundos")