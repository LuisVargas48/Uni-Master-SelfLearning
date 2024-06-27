# César Santiago Tello Correa 18011169

import heapq
import random
import timeit

def heapsort(arr):
    heap = []
    for i in arr:
        heapq.heappush(heap, i) # insertar en montículo
    sorted_arr = []
    while heap:
        sorted_arr.append(heapq.heappop(heap)) # extraer cima del montículo
    return sorted_arr

#print("Arreglo Generado: ")
arr = [random.randint(1, 1000000) for _ in range(1000000)]
#print(arr[0:10], arr[10000-10:10000])

arr = heapsort(arr)

# Medir el tiempo que tarda el algoritmo de ordenamiento de burbuja
#t = timeit.timeit(lambda: heapsort(arr), number=1)
#print("Arreglo Ordenado: ")
#print(arr[0:10], arr[10000-10:10000])
#print("Tiempo de ejecución mejor caso:", t, "segundos")

arr.reverse()
print("Arreglo Invertido: ")
#print(arr[0:10], arr[10000-10:10000])
t = timeit.timeit(lambda: heapsort(arr), number=3)
print("Tiempo de ejecución peor caso:", t, "segundos")

#random.shuffle(arr)
#print("Arreglo desordenado: ")
#print(arr[0:10], arr[10000-10:10000])
#t = timeit.timeit(lambda: heapsort(arr), number=1)
#print("Tiempo de ejecución promedio:", t, "segundos")

