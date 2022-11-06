class Recurr 
{
    public static void main(String [] args)
    {
        //for (int i = 0; i < 300; i++)
        //    System.out.println(i + " : " + F(i));
        PrintReverse(1234);
    }

    public static int F(int n)
    {
        if (n <= 0)
            return 0;
        return F(n / 10) + n % 10;
    }
    static int rev;
    public static void PrintReverse(int n)
    {
        if (n != 0)
        {
            int mod = n % 10;
            rev = rev * 10 + mod;
            PrintReverse(n/10);
        }
        else if (n == 0)
        {
            System.out.println(rev);
            return;
        }
    }
}
