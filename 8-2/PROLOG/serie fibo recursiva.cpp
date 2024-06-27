D#include "iostream"
using namespace std;


int fib(int n){

    if(n <2 )
    
         return n;

    return fib(n-1) + fib(n-2);
  }



int main(){
 int n23 ; 
cout<<"Hasta donde quieres los numeros ? "<<endl; 
cin>>n23; 
n23=fib(n23); 

for(int i =0; i <= n23; i++)
    cout << fib(i) << " ";
/*cout<<n23;*/

return 0; 
}
