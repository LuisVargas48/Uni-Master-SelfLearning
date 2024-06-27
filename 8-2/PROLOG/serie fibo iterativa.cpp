#include "iostream"
using namespace std; 

int fibo(int n){
 int n1=0; 
 int n2=1;   
int tmp; 
  if(n==0 || n==1){
  	cout<<n;
    return n; 
  }
  else{
    for(int i=1; i<n; i++){
      tmp=n1 + n2; 
      n1=n2; 
      n2=tmp;  
      cout<<tmp<<endl;
    }
  }
  return tmp; 
}

 int main(){
 int n23 ; 
cout<<"Hasta donde quieres los numeros? "<<endl; 
cin>>n23; 
n23=fibo(n23); 

return 0; 
}
