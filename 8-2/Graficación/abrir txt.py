try:
     f=open("demo.txt")
     try:
        f.write("Hola soy Luis Vargas ")
     except:
         print("Algo salio mal al escribir en el archivo")   
     finally:
         f.close()
         
except:
     print("Algo salio mal al abrir el archivo")            