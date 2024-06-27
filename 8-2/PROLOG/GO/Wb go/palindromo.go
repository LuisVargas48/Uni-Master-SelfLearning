package main
import (
  "bufio"
  "fmt"
  "os"
)
func main() {
  palabra := bufio.NewScanner(os.Stdin)
  var igual, otro int
  fmt.Print("Ingresa palabra: ")
  palabra.Scan()
  valor := palabra.Text()
  for char := len(valor) - 1; char >= 0; char-- {
    if valor[char] == valor[otro] {
      igual++
    }
    otro++
  }
  if len(valor) == igual {
    fmt.Println("Es palindromo")
  } else {
    fmt.Println("No es palindromo")
  }
}