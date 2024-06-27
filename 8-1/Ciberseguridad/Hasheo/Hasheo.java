import java.util.*; 
import java.sql.*; 
public class Hasheo{
    
    public class conexionBBDD {
         /* Declaramos 4 variables con el driver, la bbdd, usuario y contraseña*/
    private static final String driver="mysql-connector-java-5.1.15-bin.jar";
    private static final String bbdd="jdbc:mysql://localhost::3306/empleados";
    private static final String usuario ="root";
    private static final String clave="2000";
     
    /* Creamos el método para conectarnos a la base de datos. Este método
    devolverá un objeto de tipo Connection.*/
    public Connection Conexion(){
        /*Declaramos una variable para almacenar la cadena de conexión.
        Primero la iniciamos en null.*/
        Connection conex = null;
         
        //Controlamos la excepciones que puedan surgir al conectarnos a la BBDD
        try {
            //Registrar el driver
            Class.forName(driver);
            //Creamos una conexión a la Base de Datos
            conex = DriverManager.getConnection(bbdd, usuario, clave);
         
        // Si hay errores informamos al usuario. 
        } catch (Exception e) {
            System.out.println("Error al conectar con la base de datos.\n"
                    + e.getMessage().toString());
        }
        // Devolvemos la conexión.
        return conex;
    }
       
    public void main (String [] args)
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
           recursion(num);
           char [] arr=new char[num]; 
       }
       /*Declaramos una variable para almacenar la conexión que nos va a
   devolver el método Conexion(). Primero la iniciamos en null.*/
   Connection conex=null;

   /*Almacenamos lo que nos devuelve el método Conexion()
   en la variable conex*/
   conex = Conexion();

   // Si la variable objeto conex es diferente de nulo
   if(conex != null){
       // Informamos que la conexión es correcta
       System.out.println("Conectado correctamente");
   }else{ // Sino informamos que no nos podemos conectar.
       System.out.println("No has podido conectarte");
   }
    }
    }


    public static void cerrarConexion(Connection conex){
        try{
            // Cerramos la conexión
            conex.close();    
        }catch(SQLException e){
           /* Controlamos excepción en caso de que se pueda producir
            a la hora de cerrar la conexión*/
            System.out.println(e.getMessage().toString());
        }
    }

    public static void recursion(int number) {
        if(number > 0) {
            recursion(number/10);
            System.out.println(number%10);
        }


    }



}