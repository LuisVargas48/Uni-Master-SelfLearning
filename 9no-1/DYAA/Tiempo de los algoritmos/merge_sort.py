# César Santiago Tello Correa 18011169
# técnica de ordenar listas pequeñas con un algoritmo de ordenamiento más simple (Insertion Sort )

import random
import timeit


def mergesort(m):
    if len(m) <= 1:
        return m
    else:
        middle = len(m) // 2
        left = m[:middle]
        right = m[middle:]
        left = mergesort(left)
        right = mergesort(right)
        return merge(left, right)


def merge(left, right):
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result


m = [random.randint(1, 1000000) for _ in range(1000000)]
print("Arreglo Generado: ")
#print(m[0:10], m[10000-10:10000])

m = mergesort(m)


# Medir el tiempo que tarda el algoritmo de ordenamiento Merge Sort en el mejor caso
#t = timeit.timeit(lambda: mergesort(m), number=1)
#print("Arreglo Ordenado: ")
#print(m[0:10], m[10000-10:10000])
#print("Tiempo de ejecución mejor caso:", t, "segundos")

m.reverse()
#print("Arreglo Invertido: ")
#print(m[0:10], m[10000-10:10000])

# Medir el tiempo que tarda el algoritmo de ordenamiento Merge Sort en el peor caso
t = timeit.timeit(lambda: mergesort(m), number=1)
print("Tiempo de ejecución peor caso:", t, "segundos")

#random.shuffle(m)
#print("Arreglo desordenado: ")
#print(m[0:10], m[10000-10:10000])

# Medir el tiempo que tarda el algoritmo de ordenamiento Merge Sort en el promedio caso
#t = timeit.timeit(lambda: mergesort(m), number=1)
#print("Tiempo de ejecución promedio:", t, "segundos")



