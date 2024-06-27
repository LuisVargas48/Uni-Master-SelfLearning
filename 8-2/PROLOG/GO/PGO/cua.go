package main
import "fmt"

func main() {
    var n int
	fmt.Println("Indica el numero maximo para calcular el cuadrado latino ")
	fmt.Scan(&n)
	fmt.Print("\n")
   var j int
	for f := 1; f <n+1; f++ {
		for j:=f; j<n+1; j++{
              fmt.Print(j, "  \t")
		}
		if(j <n){
    
            for k:=1; k<f;k++{
			fmt.Print(k, "  \t")
		    }
			
      fmt.Println("  \n")
		}	
	}
}