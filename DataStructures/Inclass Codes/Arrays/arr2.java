import java.util.Random;

class Test
{
    public static void main(String [] args)
    {
        Integer [] arr = {1, 2, 3, 4 , 5, 6, 7, 8, 9, 0};
        Character [] arr2 = {'a', 'b', 'c', 'd', 'e', 'f', 'g'};
        Double [] arr3 = {1.1, 2.2, 3.3, 4.4, 5.5};

        iPrint(arr);
        iPrint(arr2);
        iPrint(arr3);
    }

    public static <john> void iPrint(john [] arr)
    {
        for (int i = 0; i < arr.length; i++)
        {
            System.out.print(arr[i] + ", ");
        }
        System.out.println();
    }
}
