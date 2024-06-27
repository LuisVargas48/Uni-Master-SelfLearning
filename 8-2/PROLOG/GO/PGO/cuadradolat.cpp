#include <stdio.h>
#include <stdlib.h>

int main()
{
    int n,i,j,k;
   
    printf ("ingrese el tamaño n del cuadrado: ");
    scanf ("%d",&n);
      
    for(i=1;i<=n;i++) 
        {
            for(j=i,k=1; k <=n ; k++,j++)
            {
                if (j>n) // si "j" es mayor a "n"  entonces se reinicia el contador
                {
                        for(j=1; k <= n ; k++,j++)
                        {
                              printf (" %d",j);
                        }
                }
               
                else
                     printf (" %d",j);
            }
        printf ("\n");
        }    
    system ("pause");
}
