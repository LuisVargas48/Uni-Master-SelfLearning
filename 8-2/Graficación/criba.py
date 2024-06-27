
def primos(x):
    numeros = list(range(2,x+1))
    d=0
    while numeros[d]**2 <= x:
        for n in numeros:
            if n != numeros[d]:
              if n % numeros[d] == 0:
                numeros.remove(n)
        d += 1
    return numeros
primos(1000)