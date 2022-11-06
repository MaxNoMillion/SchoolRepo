public class Hanoi 
{
    public static void main(String[] args)
    {
        Hanoi(13, 'A', 'C', 'B');
    }

    public static void Hanoi(int n, char source, char dest, char spare)
    {
        if (n == 1)
        {
            move(source, dest);
            return;
        }
        Hanoi(n-1, source, spare, dest);
        Hanoi(1, source, dest, spare);
        Hanoi(n-1, spare, dest, source);
    }

    public static void move(char source, char dest)
    {
        System.out.println(source + " -> " + dest);
    }
}
