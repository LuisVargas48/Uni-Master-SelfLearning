package main 
import "fmt"
//import "time"

func Primo(numero int){
var contador int
for i:=1;i<=numero;i++{
 if numero % i ==0{
 contador++
 }

}
if contador==2 {
 fmt.Print(numero," ")	
} 
}

func Buscar(inicio, fin int){
 for i:=inicio; i<=fin; i++{
 	Primo(i)
 }
}

	

func main () {
go Buscar(1,100000)
go Buscar(100001, 200000)
var sigue string
 fmt.Scan(&sigue);
}