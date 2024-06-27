#include <iostream>
#include <cmath>
using namespace std;
 

void criba(int n)
{
    int a[n + 1];
    int b=0;
    
    for (int i = 0; i <= n; i++) {
        a[i] = 1;
    }
 
    for (int i = 2; i <= sqrt(n); i++)
    {
        if (a[i] == 1)          
        {
            for (int j = 2; i * j <= n; j++) {
                a[i * j] = 0;   
            }
        }
    }
 
    for (int i = 2; i <= n; i++)
    {
        if (a[i] == 1 ) {
           cout << i<< " ";   
        }else(a[i]==0);{
            
            cout<<b<<" ";       
            }
    }
}
 
int main()
{
    
    criba(100);
 
    return 0;
}
