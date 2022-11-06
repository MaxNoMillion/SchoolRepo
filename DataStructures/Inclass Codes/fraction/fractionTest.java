class FractionTest
{
    public static void main(String[] args)
    {
        Fraction f1 = new Fraction();
        Fraction f2, f3, f4;
        f2 = new Fraction(1, 2);
        f3 = new Fraction(2, 4);
        f4 = new Fraction(2, 0);

        System.out.println("f1 = " + f1);
        System.out.println("f2 = " + f2);
        System.out.println("f3 = " + f3);
        System.out.println("f4 = " + f4);
    }
}