import java.util.Random;

class Test
{
    public static void main(String [] args)
    {
        int[] arr = {1, 2, 3, 4 , 5, 6, 7, 8, 9, 0};
        char[] arr2 = {'a', 'b', 'c', 'd', 'e', 'f', 'g'};
        double[] arr3 = {1.1, 2.2, 3.3, 4.4, 5.5};

        Integer a = 6, d = 8;
        Character b = 'b';
        Double c = 3.14;

        System.out.println(getMax(a, d));
        System.out.println(getMax(a, c));
        //iPrint(arr);
        //iPrint(arr2);
        //iPrint(arr3);
    }

    public static void iPrint(int[] arr)
    {
        for (int i = 0; i < arr.length; i++)
        {
            System.out.print(arr[i] + ", ");
        }
        System.out.println();
    }

    public static void iPrint(char[] arr)
    {
        for (int i = 0; i < arr.length; i++)
        {
            System.out.print(arr[i] + ", ");
        }
        System.out.println();
    }

    public static <john extends Number> john getMax(john a, john b)
    {
        if (a.floatValue() > b.floatValue())
            return a;
        return b;
    }
}
