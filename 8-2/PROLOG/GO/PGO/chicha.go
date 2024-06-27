package main 
import "fmt"
import "math"
import "html/template"
import "net/http"
import "strconv"



func chicharronera(w http.ResponseWriter, r *http.Request){
 

fmt.Println("method:", r.Method) 
    if r.Method == "GET" {
        t, _ := template.ParseFiles("raices.html")
        t.Execute(w, nil)
    } else {
        r.ParseForm()
    
       a, err := strconv.ParseFloat(r.FormValue("a"),64)
        if err != nil {
         // handle error
       }
        b,err := strconv.ParseFloat(r.FormValue("b"),64)
        if err != nil {
         // handle error
       }
        c, err := strconv.ParseFloat(r.FormValue("c"),64)
       if err != nil {
        //handle error 
       }

    var x1 float64
    var x2 float64
   
   
     

    x1=(-b+(math.Sqrt(b*b-4*a*c)))/(2*a);
    x2=(-b-(math.Sqrt(b*b-4*a*c)))/(2*a);


    fmt.Fprintf(w,"<h1>Las raices  son %f  y %f </h1>", x1,x2)
        
      }
}



func main(){
http.HandleFunc("/", chicharronera)
http.ListenAndServe(":8080", nil)
}