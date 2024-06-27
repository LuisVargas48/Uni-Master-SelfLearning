#Luis Alberto Vargas Glez. 
#19012140. 
#Selección. 
import random
import time


# codigo a medir
time.sleep(1)
def seleccion(arreglo):
    contador = 0
    longitud = len(arreglo)
    for i in range(longitud-1):
        for j in range(i+1, longitud):
            if arreglo[i] > arreglo[j]:
                arreglo[i], arreglo[j] = arreglo[j], arreglo[i]
                contador += 1
                           
    return arreglo

numeros = [random.randint(1,10000) for x in range(10000)]           

#---------

#peor caso: 
arreglo1=[x for x in range(100000)]
inicio = time.time()
arreglo1.reverse()
seleccion(arreglo1)
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