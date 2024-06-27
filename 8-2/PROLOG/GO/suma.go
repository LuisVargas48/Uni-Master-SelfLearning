package main 

import "fmt"


func main(){
	
var valor int
suma:= 0
for f := 1; f <= 10; f++{
	fmt.Print("Ingrese valor:")
	fmt.Scan(&valor)
	suma= suma + valor
}

fmt.Println("La suma es:", suma)
promedio := suma / 10
fmt.Println("El promedio es:", promedio)
}
