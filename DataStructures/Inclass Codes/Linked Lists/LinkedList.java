import java.util.Scanner;
import java.util.random;

class SS
{
    public static main(String[] args)
    {
        Scanner s = new Scanner(System.in);
        System.out.print("How many numbers do you want? ");
        int value = s.nextInt();

        int [] array = new int[value];

        Random r = new Random();
        for (int i = 0; i < array.length; i++)
            array[i] = r.nextInt(1000);
        
        myprint(array);

        System.out.println("What number are you looking for? ");
        value = s.nextInt();
        System.out.println(value + " was found at " + mysearch(array, value));
    }

    public static void myprint(int [] x)
    {
        System.out.println("___________________________________________");
        for(int i = 0; i < x.length; i++)
        {
            System.out.print(x[i] + " , ");
        }
        System.out.println("__________________________________________");
    }

    public static int mysearch(int [] arr, int val)
    {

    }
}