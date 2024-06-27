#include <iostream>
using namespace std; 
int arreglo[1000];
int n;
int datos; 
int i; 
int j; 
void criba{
while((datos[j]*datos[j]<n)){
	for(int i= j+1;i < n-1, i++ ){
		if(datos[i]% datos[j]==0){
			datos[i]=0; 
			
		  }
		break; 
		}
break; 	
   }  
 }

int main(){
cout<<"Ingresa el limite de n"<<endl;
cin>>n; 
for(i=2; i<n; i++){
    arreglo[i]=i;  
}
criba(n); 
return 0; 
}
