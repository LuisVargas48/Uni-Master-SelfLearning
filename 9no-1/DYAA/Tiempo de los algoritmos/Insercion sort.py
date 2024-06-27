#Luis Alberto Vargas Glez. 
#19012140
#Diseño y análisis de algoritmos. 
import time
import random



#codigo a medir. 
time.sleep(1)
def insercion(A):
    for i in range(len(A)):
        for j in range(i,0,-1):
            if(A[j-1] > A[j]):
                aux=A[j]
                A[j]=A[j-1]
                A[j-1]=aux
    #print (A)
    return A
 
A=[random.randint(1,10000) for x in range(10000)]



#---------

#peor caso: 
arreglo1=[x for x in range(10000)]
inicio = time.time()
arreglo1.reverse()
insercion(arreglo1)
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