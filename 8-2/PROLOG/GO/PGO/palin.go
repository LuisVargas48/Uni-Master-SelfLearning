package main

import "fmt"


func Palindromo(str string) bool {
    reversedStr := ""
    for i := len(str)-1; i >= 0; i-- {
        reversedStr += string(str[i])
    }
    for i := range(str) {
        if str[i] != reversedStr[i] {
            return false
        }
    }
    return true
}





func main () {
     var a string
    fmt.Println("Ingresa la palabra si es palindromo o no ")
	fmt.Scan(&a)
    resultado := Palindromo(a)
    fmt.Println(resultado)
}