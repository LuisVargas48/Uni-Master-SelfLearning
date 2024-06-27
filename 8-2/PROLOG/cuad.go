

import "fmt"
var m int 
func main () {

var dim int 

var k int
var p int



for {
fmt.Println("Ingresa dimension cuadrado latino")
fmt.Scan(&dim)
fmt.Print("\n")
    if dim >=2 {
    k= dim
    p=0
    m=0
        break
    }
}

	
for i :=1; i<=dim; i++{
	
	if i==1{
	 for j:=1; j<=dim; j++{
	  fmt.Print(j, "\t")
	 }
	}else{
	  for j:=k+1; j<=dim; j++{
	  fmt.Print(j, "\t")
	  }
	  for m := 1; m<=dim-p; m++{
	   fmt.Print(m,"\t")
	  }
	}
	 k = k-1
	 p=p+1
	 fmt.Print("\n")
 }
}