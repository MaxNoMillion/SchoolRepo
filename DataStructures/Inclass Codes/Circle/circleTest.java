class CircleTest
{
    public static void main(String[] args)
    {
        Circle c1 = new Circle();
        Circle c2 = new Circle(23);
        Circle c3 = new Circle(23);
        System.out.println(c2==c3);
        System.out.println(c2.Equals(c3));
    }
}