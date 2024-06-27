import random
import time
def partition(array, low, high):
 
    
    pivot = array[high]
 
    
    i = low - 1
 
   
    for j in range(low, high):
        if array[j] <= pivot:
 
            
            i = i + 1
 
            
            (array[i], array[j]) = (array[j], array[i])
 
  
    (array[i + 1], array[high]) = (array[high], array[i + 1])
 
   
    return i + 1
 

 
 
def quickSort(array, low, high):
    if low < high:
 
    
        pi = partition(array, low, high)
 
     
        quickSort(array, low, pi - 1)
 
      
        quickSort(array, pi + 1, high)

 
# promedio
arr = [random.randint(1,1000000) for x in range(1000000)]
#arr2 = arr.copy()
#inicio=time.time()
#size = len(arr2)
#quickSort(arr2,0, size - 1)
#fin=time.time()
#print("caso promedio",fin-inicio, "\n")

#peor 
arr3 = [random.randint(1,1000000) for x in range(1000000)]
arr4 = arr3.copy()
arr4.reverse()
inicio=time.time()
size2 = len(arr4)
quickSort(arr4, 0, size2 - 1)
fin=time.time()
print("peor",fin-inicio, "\n")

#mejor
#arr3 = [x for x in range(10000)]
#arr4 = arr.copy()
#arr4.reverse()
#inicio=time.time()
#size3 = len(arr4)
#quickSort(arr4, 0, size3 - 1)
#fin=time.time()
#print("mejor",fin-inicio,"\n")