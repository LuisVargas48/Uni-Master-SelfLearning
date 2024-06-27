package main

import ("fmt"
       "html/template"
    "net/http"
    "strconv"
)

func suma(w http.ResponseWriter, r *http.Request) {

    fmt.Println("method:", r.Method) 
    if r.Method == "GET" {
        t, _ := template.ParseFiles("form.html")
        t.Execute(w, nil)
    } else {
        r.ParseForm()
       

        num1, err := strconv.Atoi(r.FormValue("num1"))
        if err != nil {
      // handle error
       }
       num2, err := strconv.Atoi(r.FormValue("num2"))
        if err != nil {
      // handle error
       }
       suma:= num1+num2;

        fmt.Fprintf(w,"<h1>La suma de %d + %d es %d</h1>", num1, num2, suma)
        
      }
}

func main(){
   http.HandleFunc("/", suma)
   http.ListenAndServe(":8080", nil)
}
