import java.util.*; 
public class Prueba{

public static void main(String[] args){
    int[] inp = { 1, 2, 3, 4, 5, 6};
    int n = inp.length;

    int[] a = new int[(n + 1)/2]; // 3 numeros 
    int[] b = new int[n - a.length];

    System.arraycopy(inp, 0, a,0, a.length);
    System.arraycopy(inp, a.length, b, 0, b.length);

    System.out.println(Arrays.toString(a));
    System.out.println(Arrays.toString(b));

 }

}