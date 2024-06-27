#include "iostream"
using namespace std; 

int fibo(int n){
 int n1=0; 
 int n2=1;   
int tmp; 
  if(n==0 || n==1){
    return n; 
  }
  else{
    for(int i=1; i<n; i++){
      tmp=n1 + n2; 
      n1=n2; 
      n2=tmp; 
    }
  }
  return tmp; 
}

 int main(){
 int n ; 
cout<<"Hasta donde "<<endl; 
cin>>n; 
for(int i=1;1<n;i++){
  fibo(n); 
}   
return 0; 
}