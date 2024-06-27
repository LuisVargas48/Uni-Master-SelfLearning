import java.util.*; 
public class Hash {
    

    public  static void main (String [] args)
    { 
       try (Scanner entrada = new Scanner(System.in)) {
           System.out.println("Ingrese su numero de empleado");
           String numero = entrada.next();
           int num= 0;  
           char[] numeroEmpleado=numero.toCharArray(); 
           for (int r = 0; r < numeroEmpleado.length; r++) {
                num = num + numeroEmpleado[r];
           } 
           System.out.println("Hash de tu numero de empleado : " + num);
           //recursion(num);
           //char [] arr=new char[num]; 
       
    }


   }

    private static void recursion(int num) {
        if(num > 0) {
            recursion(num/10);
            System.out.println(num%10);
         }
    }
}
