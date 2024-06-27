#!/usr/bin/env python3
#Luis Alberto Vargas González. 
import sys
unidades= ["uno", "dos","tres", "cuatro", "cinco", 
 "seis", "siete","ocho", "nueve"]
unitario=["un"]
decesp = ["once", "doce", "trece", "catorce", "quince", "dieciseis",
 "diecisiete","dieciocho", "diecinueve"]  
decenas= ["diez", "veinte", "treinta", "cuarenta", "cincuenta", 
 "sesenta", "setenta","ochenta", "noventa"]
centenas= ["ciento", "doscientos", "trescientos", 
 "cuatrocientos", "quinientos","seiscientos","setecientos", "ochocientos","novecientos"]  
dec1=["veintiuno", "veintidos", "veintitres", "veinticuatro", "veinticinco", "veintiseis"
, "veintisiete", "veintiocho", "veintinueve"]   
cien=["cien"]
millares=["mil", "millón", "millones"]
milesdemillares=["mil millones"]
billions=["billon"]


def primeros(numeros):
    if(numeros[0]=="0"): 
        return " "
    else:
        return unidades[int(numeros[0])-1] 

def dec(numeros):
    if(numeros[0]=="0"):
        return primeros(numeros[1])
    elif(numeros[0]=="1" and numeros[1]=="0"):     
     dece=decenas[int(numeros[0])-1]
     return dece
    elif(numeros[0]=="1" and int(numeros[1])<6):
      return decesp[int(numeros[1])-1]
    elif(numeros[0]=="1" and int(numeros[1])>=6): 
      return decesp[int(numeros[1])-1]

    if(numeros[0]=="2" and numeros[1]=="0"):
     dec=decenas[int(numeros[1])-8] 
     return dec
    elif(numeros[0]=="2" and int(numeros[1])<6):
     return dec1[int(numeros[1])-1]
    elif(numeros[0]=="2" and int(numeros[1])>=6): 
        return dec1[int(numeros[1])-1] 

    if(numeros[0]=="3" and numeros[1]=="0"):
     dec=decenas[int(numeros[1])-7] 
     return dec
    elif(numeros[0]=="3" and int(numeros[1])<6):
     return decenas[int(numeros[0])-10] + " " "y" " " + unidades[int(numeros[1])-1]
    elif(numeros[0]=="3" and int(numeros[1])>=6): 
     return decenas[int(numeros[0])-10] + " " "y" " " + unidades[int(numeros[1])-1]  

    if(numeros[0]=="4" and numeros[1]=="0"):
     dec=decenas[int(numeros[1])-6] 
     return dec
    elif(numeros[0]=="4" and int(numeros[1])<6):
     return decenas[int(numeros[0])-10] + " " "y" " " + unidades[int(numeros[1])-1]
    elif(numeros[0]=="4" and int(numeros[1])>=6): 
     return decenas[int(numeros[0])-10] + " " "y" " " + unidades[int(numeros[1])-1]


    if(numeros[0]=="5" and numeros[1]=="0"):
     dec=decenas[int(numeros[1])-5] 
     return dec
    elif(numeros[0]=="5" and int(numeros[1])<6):
     return decenas[int(numeros[0])-10] + " " "y" " " + unidades[int(numeros[1])-1]
    elif(numeros[0]=="5" and int(numeros[1])>=6): 
     return decenas[int(numeros[0])-10] + " " "y" " " + unidades[int(numeros[1])-1]


    if(numeros[0]=="6" and numeros[1]=="0"):
     dec=decenas[int(numeros[1])-4] 
     return dec
    elif(numeros[0]=="6" and int(numeros[1])<6):
     return decenas[int(numeros[0])-10] + " " "y" " " + unidades[int(numeros[1])-1]
    elif(numeros[0]=="6" and int(numeros[1])>=6): 
     return decenas[int(numeros[0])-10] + " " "y" " " + unidades[int(numeros[1])-1]

    if(numeros[0]=="7" and numeros[1]=="0"):
     dec=decenas[int(numeros[1])-3] 
     return dec 
    elif(numeros[0]=="7" and int(numeros[1])<6):
     return decenas[int(numeros[0])-10] + " " "y" " " + unidades[int(numeros[1])-1]
    elif(numeros[0]=="7" and int(numeros[1])>=6): 
     return decenas[int(numeros[0])-10] + " " "y" " " + unidades[int(numeros[1])-1]
    
    if(numeros[0]=="8" and numeros[1]=="0"):
     dec=decenas[int(numeros[1])-2] 
     return dec 
    elif(numeros[0]=="8" and int(numeros[1])<6):
     return decenas[int(numeros[0])-10] + " " "y" " " + unidades[int(numeros[1])-1]
    elif(numeros[0]=="8" and int(numeros[1])>=6): 
     return decenas[int(numeros[0])-10] + " " "y" " " + unidades[int(numeros[1])-1]
     

    if(numeros[0]=="9" and numeros[1]=="0"):
     dec=decenas[int(numeros[1])-1] 
     return dec 
    elif(numeros[0]=="9" and int(numeros[1])<6):
     return decenas[int(numeros[0])-10] + " " "y" " " + unidades[int(numeros[1])-1]
    elif(numeros[0]=="9" and int(numeros[1])>=6): 
     return decenas[int(numeros[0])-10] + " " "y" " " + unidades[int(numeros[1])-1]



  
def centen(numeros):
    arreglodec=[numeros[1],numeros[2]]
    if(numeros[0]=="0"):
        return  dec(arreglodec)
    #numero 100 
    if(numeros[0]=="1" and numeros[1]=="0" and numeros[2]=="0"):
       
       cent= cien[int(numeros[1])-1]
       return cent
       #numeros de 101 a 110
    elif(numeros[0]=="1" and numeros[1]=="0" and numeros[2]>"0"):
       
       cent1= cien[int(numeros[1])-1]+ "to" + " " + unidades[int(numeros[2])-1]
       return cent1
       #numeros de 200 hasta 900 cerrados
    elif(int(numeros[0])>1 and numeros[1]=="0" and numeros[2]=="0"):
        
        cent2=centenas[int(numeros[0])-1]
        return cent2
      
    else:     
        #numeros de 201 hasta 999 
        cent3 = centenas[int(numeros[0])-1] + " "+ dec(arreglodec)
        return cent3  

def thousands(numeros): 
  if(len(numeros))==4: 
    arreglocientos=[numeros[1], numeros[2], numeros[3]]
    if(numeros[0]=="0"):
        return centen(arreglocientos)
    if(numeros[0]=="1" and numeros [1]=="0" and numeros [2]=="0" and numeros[3]=="0"):# mil 
        miles= millares[int(numeros[0])-1] 
        return miles 
    elif(numeros[0]=="1" ):# de 2 mil a 9 mil
        miles= millares[int(numeros[0])-1] + " " + centen(arreglocientos) 
        return miles 
    else: 
        miles=primeros(numeros[0])+ " mil "  + centen(arreglocientos)  
        return miles
  elif(len(numeros))==5:#decenas de miles (10 mil a 99 mil)
    arreglocientos=[numeros[2], numeros[3],numeros[4]]
    decmiles=[numeros[0], numeros[1]]
    if(numeros[0]=="0"):
        nuevomiles=[numeros[1],  numeros[2], numeros[3], numeros[4]]
        return thousands(nuevomiles)
    else: 
        ter3= dec(decmiles) + " mil " + centen(arreglocientos)    
        return ter3
  elif(len(numeros))==6:   #centenas de miles (100 mil a 999 mil)  
    arreglocientos=[numeros[3], numeros[4], numeros[5]]
    arreglocientosmiles=[numeros[0], numeros[1],numeros[2] ]
    if(numeros[0]=="0"):
        nuevomiles=[numeros[1], numeros[2], numeros[3], numeros[4], numeros[5]]
        return thousands(nuevomiles)
    else: 
        ter4= centen(arreglocientosmiles) + " mil " + centen(arreglocientos)    
        return ter4


def newmillions(numeros): 
  if(len(numeros))==7: #1 millon
    arreglomiles=[numeros[1], numeros[2], numeros[3], numeros[4], numeros[5],numeros[6]]
    if(numeros[0]=="0"):
        return thousands(arreglomiles)
    if(numeros[0]=="1" and numeros [1]=="0" and numeros [2]=="0" and numeros[3]=="0" and numeros[4]=="0" and numeros[5]=="0" and numeros[6]=="0"):# mil 
        millon= "un millon" 
        return millon  
    elif(numeros[0]=="1" ):# 1 millon y centenas de miles
        millonesprim= "un millon "+ thousands(arreglomiles) 
        return millonesprim 
    else: # de 2 millones a 9 millones
        millonesList=primeros(numeros[0]) + " millones "  + thousands(arreglomiles)  
        return millonesList
  if(len(numeros))==8:# de 10 millones a 99 millones
      arreglodec=[numeros[2], numeros[3],numeros[4], numeros[5], numeros[6], numeros[7]]
      decmillones=[numeros[0], numeros[1]]
      if(numeros[0]=="0"):
        nuevomiles=[numeros[1],  numeros[2], numeros[3], numeros[4], numeros[5], numeros[6], numeros[7]]
        return newmillions(nuevomiles)
      else: 
        ter3= dec(decmillones)  + " millones " + thousands(arreglodec)  
        return ter3
    
  if(len(numeros))==9: #de 100 millones a 999 millones
        arreglodec1=[numeros[3], numeros[4], numeros[5], numeros[6], numeros[7], numeros[8]]
        centmillones=[numeros[0],numeros[1], numeros[2]]
        if(numeros[0]=="0"):
         nuevomiles=[numeros[1],  numeros[2], numeros[3], numeros[4], numeros[5], numeros[6], numeros[7], numeros[8]]
         return newmillions(nuevomiles)
        else:
            ter4=centen(centmillones) + " millones" +"  "+ thousands(arreglodec1)
            return ter4




def newThousandmillions(numeros): 
  if(len(numeros))==10: #mil  millones
    arreglomillones=[numeros[1], numeros[2], numeros[3], numeros[4], numeros[5],numeros[6],numeros[7],numeros[8],numeros[9]]
    if(numeros[0]=="0"):
        return newmillions(arreglomillones)
    if(numeros[0]=="1" and numeros [1]=="0" and numeros [2]=="0" and numeros[3]=="0" and numeros[4]=="0" and numeros[5]=="0" and numeros[6]=="0" and numeros[7]=="0" and numeros[8]=="0" and numeros[9]=="0"):#  mil millones 
        millon= "mil millones" 
        return millon  
    elif(numeros[0]=="1" ):# mil millones y centenas de millón. 
        millonesprim= "mil "+ newmillions(arreglomillones) 
        return millonesprim 
    else: # de 2  mil millones a 9  mil millones
        arreglo2=[ numeros[1], numeros[2], numeros[3], numeros[4], numeros[5], numeros[6], numeros[7], numeros[8], numeros[9]]
        ger=primeros(numeros[0]) +"mil millones " + newmillions(arreglo2)
        return ger
  if(len(numeros))==11:# de   10 mil  millones a 99 mil  millones
      if(numeros[0]=="0"):
        nuevomiles1=[numeros[1],numeros[2], numeros[3], numeros[4], numeros[5], numeros[6], numeros[7], numeros[8], numeros[9], numeros[10]]
        return newThousandmillions(nuevomiles1)
      else: 
          arreglodec=[numeros[2], numeros[3],numeros[4], numeros[5], numeros[6], numeros[7], numeros[8], numeros[9], numeros[10]]
          decmillones=[numeros[0], numeros[1]]
          ter3= dec(decmillones)  + " mil millones " + newmillions(arreglodec)  
          return ter3
    
  if(len(numeros))==12: #de 100 mil  millones a 999 mil  millones
        arreglodec1=[numeros[3], numeros[4], numeros[5], numeros[6], numeros[7], numeros[8], numeros[9], numeros[10], numeros[11]]
        centmillones=[numeros[0],numeros[1], numeros[2]]
        if(numeros[0]=="0"):
         nuevomiles2=[numeros[1],  numeros[2], numeros[3], numeros[4], numeros[5], numeros[6], numeros[7], numeros[8], numeros[9], numeros[10], numeros[11]]
         return newThousandmillions(nuevomiles2)
        else:
            
            ter4=centen(centmillones) + " mil millones" +"  "+ newmillions(arreglodec1)
            return ter4
                
                
                
def billon(numeros): 
 if(len(numeros))==13: # 1 billón 
    bura=[numeros[1],numeros[2],numeros[3], numeros[4], numeros[5], numeros[6], numeros[7], numeros[8], numeros[9], numeros[10],numeros[11], numeros[12]]
    if(numeros[0]=="0"):
        return newThousandmillions(bura)
    if(numeros[0]=="1" and  numeros[1]=="0" and numeros[2]=="0" and numeros[3]=="0" and numeros[4]=="0" and numeros[5]=="0" and numeros[6]=="0" and numeros[7]=="0" and numeros[8]=="0" and numeros[9]=="0" and numeros[10]=="0" and numeros[11]=="0" and numeros[12]=="0"):
        bill = "un billón"
        return bill
    elif(numeros[0]=="1"): #billón y centenas de miles de millones.
        ter5= "un billón" +" " + newThousandmillions(bura)
        return ter5
    else: # de 2 billones a 9 billones. 
        birado=[numeros[1],numeros[2],numeros[3], numeros[4], numeros[5], numeros[6], numeros[7], numeros[8], numeros[9], numeros[10],numeros[11], numeros[12]]
        bill1=primeros(numeros[0]) + " billones" + " " + newThousandmillions(birado)
        return bill1


 if(len(numeros))==14: # de 10 billones a 99 billones. 
     if(numeros[0]=="0"):
         trillion=[numeros[1],numeros[2],numeros[3], numeros[4], numeros[5], numeros[6], numeros[7], numeros[8], numeros[9], numeros[10],numeros[11], numeros[12], numeros[13]]
         return billon(trillion) 
     else: 
         varity=[numeros[2],numeros[3], numeros[4], numeros[5], numeros[6], numeros[7], numeros[8], numeros[9], numeros[10],numeros[11], numeros[12], numeros[13]]
         varity1=[numeros[0], numeros[1]]
         debillones=dec(varity1) + " billones" + " " + newThousandmillions(varity) 
         return debillones
     
 if(len(numeros))==15:# de 100 billones a 999 billones.  
      if(numeros[0]=="0"): 
        cuatrillón=[numeros[1],numeros[2],numeros[3], numeros[4], numeros[5], numeros[6], numeros[7], numeros[8], numeros[9], numeros[10],numeros[11], numeros[12], numeros[13], numeros[14]]
        return billon(cuatrillón)
      else: 
          quintillón=[numeros[0], numeros[1], numeros[2]]
          sextillón=[numeros[3], numeros[4], numeros[5], numeros[6], numeros[7],numeros[8], numeros[9], numeros[10], numeros[11],numeros[12], numeros[13], numeros[14]]
          septillón= centen(quintillón) + " billones " + newThousandmillions(sextillón)
          return septillón 
               
    


def a_numero(numero):
    if(len(numero))==1:
     numero_en_letra=primeros(numero)  
     return numero_en_letra
    elif(len(numero))==2:
     numero_en_letra=dec(numero)
     return numero_en_letra
    elif(len(numero))==3: 
     numero_en_letra=centen(numero)
     return numero_en_letra
    elif(len(numero))==4:
     numero_en_letra=thousands(numero)     
     return numero_en_letra
    elif(len(numero))==5: 
     numero_en_letra=thousands(numero)
     return numero_en_letra
    elif(len(numero))==6: 
     numero_en_letra=thousands(numero)
     return numero_en_letra
    elif(len(numero))==7: 
     numero_en_letra=newmillions(numero)
     return numero_en_letra
    elif(len(numero))==8: 
     numero_en_letra=newmillions(numero)
     return numero_en_letra
    elif(len(numero))==9: 
        numero_en_letra=newmillions(numero)
        return numero_en_letra
    elif(len(numero))==10: 
        numero_en_letra=newThousandmillions(numero)
        return numero_en_letra
    elif(len(numero))==11:
        numero_en_letra=newThousandmillions(numero)
        return numero_en_letra
    elif(len(numero))==12: 
        numero_en_letra=newThousandmillions(numero)
        return numero_en_letra
    elif(len(numero))==13: 
        numero_en_letra=billon(numero)  
        return numero_en_letra
    elif(len(numero))==14: 
        numero_en_letra=billon(numero)
        return numero_en_letra
    elif(len(numero))==15: 
        numero_en_letra=billon(numero)
        return numero_en_letra
       
     
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Necesitas un argumento")
    else:
        num = a_numero(str(sys.argv[1]))
        print("En letra:", num)